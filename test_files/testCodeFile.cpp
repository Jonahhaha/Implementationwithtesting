// Generate C code for sorting a dynamic 2x2 arrays based off of double values in the first column.
// The array is sorted in ascending order.

// Read in array
double array[2][2];
for (int i = 0; i < 2; i++) {
    for (int j = 0; j < 2; j++) {
        array[i][j] = 0;
    }
}

// Sort array
for (int i = 0; i < 2; i++) {
    for (int j = 0; j < 2; j++) {
        for (int k = 0; k < 2; k++) {
            for (int l = 0; l < 2; l++) {
                if (array[i][j] < array[k][l]) {
                    double temp = array[i][j];
                    array[i][j] = array[k][l];
                    array[k][l] = temp;
                }
            }
        }
    }
}