document.addEventListener('DOMContentLoaded', function() {
    const makeField = document.getElementById('id_make');  
    const modelField = document.getElementById('id_model'); 
  
    // изначально делаем модель неактивной
    if (modelField) {
        modelField.disabled = true;
    }

    // отслеживаем изменения в поле make
    if (makeField) {
        makeField.addEventListener('change', function() {
            if (makeField.value) {
                modelField.disabled = false;  
                
                updateModelOptions(makeField.value);
            } else {
                modelField.disabled = true;  
                modelField.value = '';  
            }
        });
    }
    // если мы редактируем и марка уже выбрана, то model разблокируется
    if (window.location.pathname.endsWith('change/')) {
        console.log('something')
        if (makeField.value){
            makeId = makeField.value
            modelField.disabled = false;
            updateModelOptions(makeId)
        }
    }

    function updateModelOptions(makeId) {
        fetch('/get-models/?make_id=' + makeId) 
            .then(response => response.json())
            .then(data => {
                const currentValue = modelField.value; // Сохраняем текущее значение
                
    
                modelField.innerHTML = ''; // Очищаем текущие опции
                
                data.forEach(model => {
                    const option = document.createElement('option');
                    option.value = model.id;
                    option.textContent = model.name;
                    modelField.appendChild(option);
                });
    
                // Восстанавливаем текущее значение, если оно существует в новых опциях
                if (currentValue) {
                    modelField.value = currentValue; 
                }
            });
    }
})