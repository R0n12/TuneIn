var coll = document.getElementsByClassName("collapsible");
var currText= 0
for (let i = 0; i < coll.length; i++) {
    coll[i].addEventListener("click", function () {
        this.classList.toggle("active");

        var content = this.nextElementSibling;

        if (content.style.maxHeight) {
            content.style.maxHeight = null;
        } else {
            content.style.maxHeight = content.scrollHeight + "px";
        }

    });
}

function getTime() {
    let today = new Date();
    hours = today.getHours();
    minutes = today.getMinutes();

    if (hours < 10) {
        hours = "0" + hours;
    }

    if (minutes < 10) {
        minutes = "0" + minutes;
    }

    let time = hours + ":" + minutes;
    return time;
}

// Gets the first message
function firstBotMessage() {
    let firstMessage = "What is you favorite music?"
    document.getElementById("botStarterMessage").innerHTML = '<p class="botText"><span>' + firstMessage + '</span></p>';

    let time = getTime();

    $("#chat-timestamp").append(time);
    document.getElementById("userInput").scrollIntoView(false);
}

firstBotMessage();

// Retrieves the response
function getHardResponse(userText) {
   //let botResponse = getBotResponse(userText);
    var message = currText
    
     $.ajax({
        url:"http://127.0.0.1:8081/user_input",
        type:"GET",
        data:{
            message:message
        },
        success:function (data) {
            console.log(String(data.message))
           
           let botHtml = '<p class="botText"><span>' + String(data.message) + '</span></p>';
   
    $("#chatbox").append(botHtml);

    document.getElementById("chat-bar-bottom").scrollIntoView(true);
        },
        error:function () {
            alert(String(data.message))
        }
    })
    
}

function getBotResponse(userText) {
    var message = currText
    var recs = 0
     $.ajax({
        url:"http://127.0.0.1:8081/user_input",
        type:"GET",
        data:{
            message:message
        },
        success:function (data) {
            console.log(String(data.message))
           recs =  String(data.message)
        },
        error:function () {
            alert(String(data.message))
        }
    })

    

    return recs
    // $.getJSON("http://127.0.0.1:8081/change_to_json",function (data) {
           
    //        return String(data.message) //show backend data in frontend
            
    // })
    
    // $.ajax({
    //     type : "GET",
    //     url : 'http://127.0.0.1:8081/change_to_json',
        
    //     success: function (data) {
    //         alert(data+ "yo");
    //         return data
    //         }
    //     ,
    //     error:function () {
    //         console.log("Fail to get the input from api")
    //     }
    // });
   

}

//Gets the text text from the input box and processes it
function getResponse() {
    let userText = $("#textInput").val();
    currText = userText
    if (userText == "") {
        userText = "";
    }

    let userHtml = '<p class="userText"><span>' + userText + '</span></p>';

    $("#textInput").val("");
    $("#chatbox").append(userHtml);
    document.getElementById("chat-bar-bottom").scrollIntoView(true);

  
    getHardResponse(userText);
  
    
}

// Handles sending text via button clicks
function buttonSendText(sampleText) {
    let userHtml = '<p class="userText"><span>' + sampleText + '</span></p>';

    $("#textInput").val("");
    $("#chatbox").append(userHtml);
    document.getElementById("chat-bar-bottom").scrollIntoView(true);

    //Uncomment this if you want the bot to respond to this buttonSendText event
    // setTimeout(() => {
    //     getHardResponse(sampleText);
    // }, 1000)
}

function sendButton() {
    getResponse();
}

function heartButton() {
    buttonSendText("Heart clicked!")
}

// Press enter to send a message
$("#textInput").keypress(function (e) {
    if (e.which == 13) {
        getResponse();
    }
});