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
   
    
    if (makeField.value){
        makeId = makeField.value
        modelField.disabled = false;
        if (modelField.value){
            modelId = modelField.value
            updateModelOptions(makeId)
        }
        else{
            updateModelOptions(makeId)
        }
        
    }
    

    function updateModelOptions(makeId) {
        fetch('/get-models/?make_id=' + makeId) 
            .then(response => response.json())
            .then(data => {
                const currentValue = modelField.value;
                modelField.innerHTML = ''; 
                data.forEach(model => {
                    const option = document.createElement('option');
                    option.value = model.id;
                    option.textContent = model.name;
                    modelField.appendChild(option);
                });
                modelField.value = ''
                if (currentValue) {
                    modelField.value = currentValue; 
                }
            });
    }
})