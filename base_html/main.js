
function hoverin(id) {
	document.getElementById(id).style.display = "block";
}

function hoverout(id) {
	document.getElementById(id).style.display = "none";
}

function myFunction(event, id) {
    parent = document.getElementById(id).parentElement;
    
	if (document.getElementById(id).style.display == "block" && parent.onmouseover != null) {
        document.getElementById(id).style.display = "block";
		parent.onmouseover= null;
		parent.onmouseout= null;
        
	} else if (document.getElementById(id).style.display == "block" && parent.onmouseover == null) {
        document.getElementById(id).style.display = "none";
		parent.setAttribute("onmouseover", `hoverin("${id}")`);
		parent.setAttribute("onmouseout", `hoverout("${id}")`);
    }
    
    event.stopImmediatePropagation();
}


var modal = document.getElementById("myModal");

function buttonclick(event, btn_id){
	var img = document.getElementById(btn_id);
	var modalImg = document.getElementById("img01");
	var captionText = document.getElementById("caption");

	modal.style.display = "block";
	modalImg.src = img.src;
	captionText.innerHTML = img.alt;

	var span = document.getElementsByClassName("close")[0];

	span.onclick = function() { 
		modal.style.display = "none";
    }
    
    event.stopImmediatePropagation();
}