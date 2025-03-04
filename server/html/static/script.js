function generateURL(){
    const id = document.getElementById('studentId').value;
    
    const url = `http://localhost:8000/api/student/${id}`;
    document.getElementById('url_gen').innerHTML = url;
}