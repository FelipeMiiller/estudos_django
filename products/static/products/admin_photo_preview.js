document.addEventListener('DOMContentLoaded', function() {
  const photoInput = document.getElementById('id_photo');
  if (!photoInput) return;

  // Cria o elemento de preview se não existir
  let preview = document.getElementById('photo-preview');
  if (!preview) {
    preview = document.createElement('img');
    preview.id = 'photo-preview';
    preview.style.width = '100px';
    preview.style.height = '100px';
    preview.style.borderRadius = '50%';
    preview.style.objectFit = 'cover';
    preview.style.display = 'block';
    preview.style.marginBottom = '10px';
    // Insere antes do input
    photoInput.parentNode.insertBefore(preview, photoInput);
  }

  // Atualiza o preview quando trocar o arquivo
  photoInput.addEventListener('change', function(e) {
    const file = e.target.files[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = function(evt) {
        preview.src = evt.target.result;
        preview.style.display = 'block';
      };
      reader.readAsDataURL(file);
    } else {
      preview.src = '';
      preview.style.display = 'none';
    }
  });

  // Esconde preview se não houver imagem
  if (!photoInput.value) {
    preview.style.display = 'none';
  }
});
