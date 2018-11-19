CKEDITOR.editorConfig = function(config) {
  config.toolbar_Default = [
    ['Styles', 'Format', 'Bold', 'Italic', 'Underline', 'Strike', 'Undo', 'Redo'],
    ['Link', 'Unlink', 'Anchor'],
    ['Image', 'Table', 'HorizontalRule'],
    ['TextColor', 'BGColor'],
    ['Smiley', 'SpecialChar'], ['Source']
  ];
  config.filebrowserBrowseUrl = '/ckeditor/browse/';
  config.filebrowserUploadUrl = '/ckeditor/upload/';
  // config.filebrowserWindowWidth = '90%';
  // config.filebrowserWindowHeight = '80%';
};
