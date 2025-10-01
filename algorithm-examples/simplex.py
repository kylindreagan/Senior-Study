from math import isclose

EPS = 1e-9

class SimplexResult:
    def __init__(self, status, objective=None, x=None):
        # status: "optimal", "infeasible", "unbounded"
        self.status = status
        self.objective = objective
        self.x = x or []

    def __repr__(self):
        return f"SimplexResult(status={self.status!r}, objective={self.objective}, x={self.x})"

def _pivot(tableau, row, col):
    """Perform pivot on tableau at (row, col). Modifies tableau in-place."""
    pivot_val = tableau[row][col]
    assert abs(pivot_val) > EPS, "Pivot is too small"
    # normalize pivot row
    tableau[row] = [v / pivot_val for v in tableau[row]]
    # eliminate other rows
    m = len(tableau)
    n = len(tableau[0])
    for r in range(m):
        if r != row:
            factor = tableau[r][col]
            if abs(factor) > EPS:
                tableau[r] = [tableau[r][c] - factor * tableau[row][c] for c in range(n)]

def _find_pivot_column(objective_row, basic_vars_idx):
    """Bland's rule isn't strictly required; choose most negative coefficient (max improvement)."""
    # objective_row is the last row (for max problems we use neg coeffs)
    # return index (col) of entering variable or None if optimal
    best = None
    best_val = 0
    for j, val in enumerate(objective_row[:-1]):  # exclude RHS column
        if val < -EPS and (best is None or val < best_val):
            best = j
            best_val = val
    return best

def _find_pivot_row(tableau, col):
    """Find leaving variable row using minimum ratio test. Return None if unbounded."""
    m = len(tableau)
    n = len(tableau[0])
    min_ratio = None
    min_row = None
    for i in range(m - 1):  # each constraint row; last row is objective
        a_ij = tableau[i][col]
        if a_ij > EPS:
            rhs = tableau[i][-1]
            ratio = rhs / a_ij
            if ratio >= -EPS:
                if min_ratio is None or ratio < min_ratio - EPS or (isclose(ratio, min_ratio) and i < min_row):
                    min_ratio = ratio
                    min_row = i
    return min_row

def _extract_solution(tableau, basic_vars, num_original_vars):
    m = len(tableau)
    n = len(tableau[0])
    x = [0.0] * num_original_vars
    for var_idx, row in basic_vars.items():
        if var_idx < num_original_vars:
            x[var_idx] = tableau[row][-1]
    obj = tableau[-1][-1]
    return obj, x

def two_phase_simplex(c, A, b, signs):
    """
    Solve: maximize c^T x subject to A x (signs[i]) b[i], x >= 0
    - c: list of objective coefficients (length n)
    - A: list of rows (m x n)
    - b: RHS list (length m)
    - signs: list of constraint signs, each one of '<=', '>=', '='
    Returns SimplexResult.
    """
    # Validate shapes
    m = len(A)
    n = len(c)
    assert len(b) == m and len(signs) == m

    # Convert constraints: ensure b >= 0 by multiplying row by -1 if needed
    A2 = [row[:] for row in A]
    b2 = b[:]
    s2 = signs[:]
    for i in range(m):
        if b2[i] < -EPS:
            # multiply row by -1 and flip sign
            A2[i] = [-a for a in A2[i]]
            b2[i] = -b2[i]
            if s2[i] == '<=':
                s2[i] = '>='
            elif s2[i] == '>=':
                s2[i] = '<='
            # '=' stays '='

    # Build initial tableau with slack/excess and artificial variables
    # We'll maintain order of columns: [original vars..., slack/excess..., artificial..., RHS]
    slack_count = 0
    artificial_count = 0
    slack_indices = []
    artificial_indices = []

    # Determine how many slacks/excess/artificial needed
    for sign in s2:
        if sign == '<=':
            slack_count += 1
        elif sign == '>=':
            slack_count += 1  # we add an excess (negative slack) and an artificial
            artificial_count += 1
        elif sign == '=':
            artificial_count += 1

    total_vars = n + slack_count + artificial_count
    # Build zero-initialized tableau: m constraint rows + 1 objective row, columns = total_vars + 1 (RHS)
    tableau = [[0.0] * (total_vars + 1) for _ in range(m + 1)]

    # Keep track: basic variable for each constraint row (var_index -> row)
    basic_vars = {}

    slack_pos = n
    art_pos = n + slack_count

    for i in range(m):
        # original variables coefficients
        for j in range(n):
            tableau[i][j] = A2[i][j]
        # RHS
        tableau[i][-1] = b2[i]
        # handle sign
        if s2[i] == '<=':
            # add slack variable +1, becomes basic
            tableau[i][slack_pos] = 1.0
            basic_vars[slack_pos] = i
            slack_pos += 1
        elif s2[i] == '>=':
            # add excess variable (-1) and artificial +1
            tableau[i][slack_pos] = -1.0  # excess var (not basic)
            tableau[i][art_pos] = 1.0
            basic_vars[art_pos] = i  # artificial is basic
            slack_pos += 1
            art_pos += 1
        elif s2[i] == '=':
            # add artificial var only
            tableau[i][art_pos] = 1.0
            basic_vars[art_pos] = i
            art_pos += 1

    # Phase I: minimize sum of artificials => equivalently maximize negative sum
    # Build objective row for phase I
    # objective row should be sum of negative of artificial rows (to make artificials' coefficients zero in basis)
    # We'll make objective row for maximization scheme: maximize (-sum artificials) so that at optimum objective = -sum(artificial values)
    # Initialize objective row with zeros
    phase1_row = [0.0] * (total_vars + 1)
    # For each artificial var that is basic, add (-1) * that constraint row to objective row
    for var_idx, row in list(basic_vars.items()):
        if var_idx >= n + slack_count:  # it's an artificial variable
            # subtract the row from objective (because we maximize negative sum)
            for col in range(total_vars + 1):
                phase1_row[col] -= tableau[row][col]
    tableau[-1] = phase1_row

    # Record which columns correspond to artificial variables for later removal
    artificial_cols = list(range(n + slack_count, n + slack_count + artificial_count))

    # If there are artificials, we must run phase I; otherwise skip
    def run_simplex(tableau, basic_vars, allow_unbounded=False):
        """
        Run simplex on the provided tableau. The tableau uses maximization form.
        Returns a tuple (status, tableau, basic_vars)
        status: "optimal" or "unbounded"
        """
        while True:
            entering = _find_pivot_column(tableau[-1], basic_vars)
            if entering is None:
                return "optimal", tableau, basic_vars
            leaving = _find_pivot_row(tableau, entering)
            if leaving is None:
                return "unbounded", tableau, basic_vars
            # Update basic vars map: find variable leaving (col index in basic_vars)
            # Remove any existing var that maps to leaving row
            to_remove = None
            for var, r in basic_vars.items():
                if r == leaving:
                    to_remove = var
                    break
            if to_remove is not None:
                del basic_vars[to_remove]
            basic_vars[entering] = leaving
            _pivot(tableau, leaving, entering)

    if artificial_count > 0:
        status, tableau, basic_vars = run_simplex(tableau, basic_vars, allow_unbounded=False)
        if status == "unbounded":
            # If phase I is unbounded, something is odd; treat as infeasible
            return SimplexResult("infeasible")
        # Check phase I objective value: tableau[-1][-1] is max(-sum artificials)
        phase1_obj = tableau[-1][-1]
        # Because we maximized negative sum of artificials, optimal value should be approximately 0 for feasibility
        if abs(phase1_obj) > 1e-7:
            # infeasible
            return SimplexResult("infeasible")
        # Remove artificial columns from tableau
        # But first, if any artificial is basic, we must pivot it out using a non-artificial entering variable.
        for art_col in artificial_cols:
            if art_col in basic_vars:
                row = basic_vars[art_col]
                # find a non-artificial column with non-zero coeff in this row to pivot in
                pivot_col = None
                for j in range(n + slack_count):  # only original + slack/excess
                    if abs(tableau[row][j]) > EPS:
                        pivot_col = j
                        break
                if pivot_col is not None:
                    # replace basic var
                    del basic_vars[art_col]
                    basic_vars[pivot_col] = row
                    _pivot(tableau, row, pivot_col)
                else:
                    # entire row zero except artificial -> variable is redundant; drop artificial
                    del basic_vars[art_col]
        # Now actually remove artificial columns from tableau structure
        # Build new tableau removing artificial columns
        keep_cols = [j for j in range(total_vars) if j not in artificial_cols] + [total_vars]  # keep RHS at end
        new_nvars = len(keep_cols) - 1
        new_tableau = []
        for r in range(len(tableau)):
            new_row = [tableau[r][j] for j in keep_cols]
            new_tableau.append(new_row)
        # Remap basic_vars indices to new column indices
        new_basic = {}
        col_map = {}
        new_idx = 0
        for j in range(total_vars):
            if j not in artificial_cols:
                col_map[j] = new_idx
                new_idx += 1
        for var, row in basic_vars.items():
            if var in col_map:
                new_basic[col_map[var]] = row
        tableau = new_tableau
        basic_vars = new_basic
        total_vars = new_nvars

    # Phase II: build real objective row (maximize c^T x)
    # objective row should be negative coefficients for maximization scheme (we put them directly because our tableau uses maximize)
    obj_row = [0.0] * (total_vars + 1)
    # place c in columns corresponding to original variables
    for j in range(n):
        if j < total_vars:
            obj_row[j] = -c[j]  # we will maximize; tableau convention: last row contains coefficients that are subtracted
    # If some basic variables correspond to original variables or slacks, we need to make objective row consistent:
    # subtract basic rows times their coefficient in obj_row so that basic variables have 0 coefficient in objective row
    for var, row in list(basic_vars.items()):
        coef = obj_row[var] if var < len(obj_row) - 1 else 0.0
        if abs(coef) > EPS:
            for col in range(len(obj_row)):
                obj_row[col] -= coef * tableau[row][col]
    tableau[-1] = obj_row

    # Run Phase II simplex
    status, tableau, basic_vars = run_simplex(tableau, basic_vars, allow_unbounded=True)
    if status == "unbounded":
        return SimplexResult("unbounded")

    # Extract solution
    obj, x = _extract_solution(tableau, basic_vars, n)
    return SimplexResult("optimal", objective=obj, x=x)

# ---------------------------
# Example usage
# ---------------------------
if __name__ == "__main__":
    # Example 1:
    # maximize 3x + 2y
    # s.t.
    # x + y <= 4
    # x + 3y <= 6
    # x, y >= 0
    c = [3, 2]
    A = [
        [1, 1],
        [1, 3]
    ]
    b = [4, 6]
    signs = ['<=', '<=']
    res = two_phase_simplex(c, A, b, signs)
    print("Example 1:", res)

    # Example 2: equality constraint and >= constraint
    # maximize x + y
    # s.t.
    # x + y = 5
    # x - y >= 1
    c2 = [1, 1]
    A2 = [
        [1, 1],
        [1, -1]
    ]
    b2 = [5, 1]
    signs2 = ['=', '>=']
    res2 = two_phase_simplex(c2, A2, b2, signs2)
    print("Example 2:", res2)
