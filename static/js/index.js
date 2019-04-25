/*
    read iinput user image and show it.
*/
function readURL(input) {
    if (input.files && input.files[0]) {
        var reader = new FileReader();

        reader.onload = function (e) {
            $('#imag_1')
                .attr('src', e.target.result)
                .width(150)
                .height(200);
        };

        reader.readAsDataURL(input.files[0]);
    }
}
/*
    show the drop down if user want to apply denoising.
*/
function denoising_disply() {
    // Get the checkbox
    var checkBox = document.getElementById("Denoising");
    // Get the output text
    var choice = document.getElementById("choice");
  
    // If the checkbox is checked, display the output text
    if (checkBox.checked == true){
        choice.style.display = "block";
    } else {
        choice.style.display = "none";
    }
}


/*
    check if the user choice an image or not.
*/
function validateForm(){
    if(!document.getElementById('InputImage').value) {
       document.getElementById('msg').style.display = "block";
       return false;
    }
}

