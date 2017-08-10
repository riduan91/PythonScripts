var operations = ['simplification', 'addition', 'substraction', 'multiplication', 'bidegree_calculation']

function ChooseOperation() {
    for (var i = 0; i < operations.length; i++){
        if (document.getElementById('selection_' + operations[i]).selected) {
            document.getElementById('input_' + operations[i]).style.display = "block";
        }
        else {
            document.getElementById('input_' + operations[i]).style.display = "none";
        }
    }
}