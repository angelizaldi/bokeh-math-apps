filterObjects("all");

// The filterObjects function takes in a parameter "c"
// If the value passed in is "all", it sets the value of c to an empty string
// It then selects all elements with the class "col" and assigns it to the variable x
// A for loop then iterates through the elements in x
// For each iteration, the element's "show" class is removed using the removeClass function
// Then, the element's className is checked if it contains the value of "c"
// If it does, the element's "show" class is added using the addClass function

function filterObjects(c) {
  var x, i;
  x = document.getElementsByClassName("col");
  console.log(x[0].className.indexOf('linalg'))
  if (c == "all") c = "";
  for (i = 0; i < x.length; i++) {
    removeClass(x[i], "show");
    if (x[i].className.indexOf(c) > -1) addClass(x[i], "show");
  }
}

// The addClass function takes in an element and a class name to be added
// It splits the element's current className and the class name to be added into arrays
// A for loop then iterates through the class name to be added
// For each iteration, it checks if the class name is already present in the element's className
// If it is not, it adds the class name to the element's className

function addClass(element, name) {
    var i, arr1, arr2;
    arr1 = element.className.split(" ");
    arr2 = name.split(" ");
    for (i = 0; i < arr2.length; i++) {
        if (arr1.indexOf(arr2[i]) == -1) {
            element.className += " " + arr2[i];
        }
    }
}

// The removeClass function takes in an element and a class name to be removed
// It splits the element's current className and the class name to be removed into arrays
// A for loop then iterates through the class name to be removed
// For each iteration, it checks if the class name is present in the element's className
// If it is, it removes the class name from the element's className

function removeClass(element, name) {
    var i, arr1, arr2;
    arr1 = element.className.split(" ");
    arr2 = name.split(" ");
    for (i = 0; i < arr2.length; i++) {
        while (arr1.indexOf(arr2[i]) > -1) {
            arr1.splice(arr1.indexOf(arr2[i]), 1);
        }
    }
    element.className = arr1.join(" ");
}
