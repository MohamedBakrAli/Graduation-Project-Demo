var x2, x3, x4;
function PrintImage(source)
{
    Pagelink = "about:blank";
    var pwa = window.open(Pagelink, "_new");
    pwa.document.open();
    pwa.document.write(ImagetoPrint(source));
    pwa.document.close();
}

function readURL(input) {
    if (input.files && input.files[0]) {
        var reader = new FileReader();
        
        reader.onload = function (e) {
            $('#image_1')
                .attr('src', e.target.result);
            
                PrintImage(e.target.result)
           
            
        };
        console.log(reader.readAsArrayBuffer());
        reader.readAsDataURL(input.files[0]);
        
        
    }
}

function button_cliked(id) {
    x2 = 0;
    x3 = 0;
    x4 = 0;
    if (id == 2){
        x2 = 2;
    }
    else if (id == 3){
        x3 = 3;
    }
    else if (id == 4){
        x4 =4;
    }
}

function update_drop_buttons(value) {
    document.getElementById("drop_btn").value = value;
    document.getElementById("drop_btn").innerHTML = value;
}





function  submit_input() {
  
    var input_image = document.getElementById("image_1").src;
    var denoising = document.getElementById("drop_btn").value;
    var url = "/demo";
    
    PrintImage(input_image);

    var scale = Math.max(x2, x3, x4);
    event.preventDefault();
    var request = new XMLHttpRequest();            
    request.open("POST", url, true);
    request.setRequestHeader("Content-Type", "application/json");
    

    var data = JSON.stringify({image:input_image, denoising : denoising, scale : scale});

    console.log(data);
    request.send(data);
}




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


