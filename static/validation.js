function validateForm() {
    let password = document.getElementById("password").value;
    let errorMessage = ""; 

    const minLength = 8;
    const uppercaseRegex = /[A-Z]/;
    const lowercaseRegex = /[a-z]/;
    const numberRegex = /[0-9]/;
    const specialCharRegex = /[@#$%^&*!]/;

    if (password.length < minLength) {
        errorMessage = "Password must be at least 8 characters long.";
    } else if (!uppercaseRegex.test(password)) {
        errorMessage = "Password must contain at least one uppercase letter.";
    } else if (!lowercaseRegex.test(password)) {
        errorMessage = "Password must contain at least one lowercase letter.";
    } else if (!numberRegex.test(password)) {
        errorMessage = "Password must contain at least one number.";
    } else if (!specialCharRegex.test(password)) {
        errorMessage = "Password must contain at least one special character (@, #, $, %, etc.).";
    }

    if (errorMessage !== "") {
        alert(errorMessage); 
        return false; 
    }

    return true; 
}
