const inputsPasswords = document.querySelectorAll(".input-password");

inputsPasswords.forEach((input, _, parent) => {
  input.children[1].addEventListener("click", (event) => {
    if (input.children[0].getAttribute("type") == "password") {
      input.children[0].setAttribute("type", "text");
      input.children[1].classList.replace("bi-eye-fill", "bi-eye-slash-fill");
      return;
    }
    input.children[0].setAttribute("type", "password");
    input.children[1].classList.replace("bi-eye-slash-fill", "bi-eye-fill");
  });
});

imagesInputs = document.querySelectorAll('[accept="image/*"]');

imagesInputs.forEach((input) => {
  input.addEventListener("change", (event) => {
    const [file] = input.files;
    if (file) {
      input.parentElement.children[1].children[0].src = URL.createObjectURL(file);
    }
  });
});
