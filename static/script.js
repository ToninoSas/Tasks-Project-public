let form = $('#new-task');
let task_container = $("#task-container");

function createTask() {
    if (task_container.children('table').length > 0) {
        task_container.empty()
    }

    form.show();
}

form.on('submit', (event) => {
    event.preventDefault();

    saveTask();
})


function saveTask() {

    let url = $('input[name="url"]').val();
    let desc = $('textarea').val()

    if (url == "") {
        alert('Campo url vuoto!')
        return;
    }

    let data = {
        link: url,
        desc:desc
    }

    $.post('http://localhost:5000/output', data, function (data, status) {
        
        if(data == "false"){
            alert('Errore nel salvare la task. Controlla che il link sia valido')
        }else{
            alert('Task Salvata!')
            form.hide()
        }        
    })

}
