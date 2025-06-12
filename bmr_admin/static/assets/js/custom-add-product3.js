(function () {
  // snow editor
  var editor5 = new Quill("#editor5", {
    modules: { toolbar: "#toolbar5" },
    theme: "snow",
    placeholder: "Enter your messages...",
  });

  // bubble editor
  var editor6 = new Quill("#editor6", {
    modules: { toolbar: "#toolbar6" },
    theme: "bubble",
    placeholder: "Enter your messages...",
  });

  // standard editor
  var editor7 = new Quill("#editor7", {
    modules: { toolbar: "#toolbar7" },
    theme: "snow",
    placeholder: "Enter your messages...",
  });

  // Set initial content from textarea
  const initialContent = document.getElementById("descriptionInput").value;
  editor7.root.innerHTML = initialContent;

  // Sync the Quill content to the textarea on change
    editor7.on('text-change', function () {
      document.getElementById("descriptionInput").value = editor7.root.innerHTML;
    });

    // OR — If using in a <form>, sync just before submit
    document.querySelector("form").addEventListener("submit", function () {
      document.getElementById("descriptionInput").value = editor7.root.innerHTML;
    });

})();
