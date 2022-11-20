var addfrdbtn = document.getElementById("addfrd");
const searchBar=document.getElementById("searchBar");
const chatlist=document.getElementsByClassName("block");
const addFrdBtn=document.getElementById("addFrdBtn");
const sendMsg=document.getElementById("enterMsg");
const sendMsgBtn=document.getElementById("send");
const getuser=document.getElementById("targetUser");
const blcokarray=[];
var selected=null;
addfrdbtn.onclick = function() {
    btn = document.getElementById("addform");
    btn.classList.toggle('active');
}


//document.addEventListener('click',(e)=>{
 //   console.log(e.target.id);
//})

function to_ppl(id){
    console.log(id)
    if(selected!=null){
        selected.classList.remove('active')
    }
    document.getElementById(id).classList.add('active');
    selected=document.getElementById(id);
}

sendMsg.addEventListener('keyup',(e)=>{

    var data='message=' + e.target.value+"&"+'receiver='+getuser.innerText;
    console.log(data);
    if (event.keyCode === 13){
        e.target.value='';
        fetch("/chat/message", {
            method: "POST",
            headers: {'Content-Type': 'application/x-www-form-urlencoded'}, 
            body: data
          }).then(res => {
          });
        location.reload();
    }
})

sendMsgBtn.addEventListener('click',(e)=>{
    var data='message=' + sendMsg.innerText+"&"+'receiver='+getuser.innerText;
    fetch("/chat/message", {
        method: "POST",
        headers: {'Content-Type': 'application/x-www-form-urlencoded'}, 
        body: data
      }).then(res => {
      });
      location.reload();
})
function refreshPage()
    {
        window.location = window.location.href;
    }
setInterval('refreshPage()', 5000);
