document.addEventListener('DOMContentLoaded', function () {
  document.querySelectorAll('p.file-upload').forEach(function (p) {
    // Atualmente: <a href=...>
    const link = p.querySelector('a');
    const imgDefault = {
      width: '100px',
      height: '100px',
      objectFit: 'cover',
      display: 'block',
      margin: '6px 0'
    };

    if (link) {
      const url = link.getAttribute('href');
      // Cria img da imagem atual
      let imgAtual = document.createElement('img');
      imgAtual.src = url;
      Object.assign(imgAtual.style, imgDefault);

      link.insertAdjacentElement('afterend', imgAtual);
    }
    // Modificar: <input type=file ...>
    const fileInput = p.querySelector('input[type="file"]');
    if (fileInput) {
      // Cria img de preview
      let preview = document.createElement('img');
      Object.assign(preview.style, imgDefault);
      preview.style.display = 'none';

      fileInput.insertAdjacentElement('beforebegin', preview);
      fileInput.addEventListener('change', function (e) {
        const file = e.target.files[0];
        if (file) {
          const reader = new FileReader();
          reader.onload = function (evt) {
            preview.src = evt.target.result;
            preview.style.display = 'block';
          };
          reader.readAsDataURL(file);
        } else {
          preview.src = '';
          preview.style.display = 'none';
        }
      });
    }
  });
});