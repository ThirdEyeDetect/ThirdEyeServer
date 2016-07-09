
var RSAencrypt = new JSEncrypt();

RSAencrypt.setPrivateKey();

$(document).ready(function(){
    sendGetRequestToServlet()
});

function sendGetRequestToServlet(){
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (xhttp.readyState == 4 && xhttp.status == 200){
            if(xhttp.response === "---End---"){return};
            var document = JSON.parse(xhttp.response)
            document = decryptDocument(document);
            console.dir(document);
            returnDocumentToServer(document)
            setTimeout(sendGetRequestToServlet,100);
        }
    }
    xhttp.open("POST","/getDocument",false);
    xhttp.send();
    
}

function decryptDocument(document){
    if(!document.hasOwnProperty('EncryptedRandomKey')){return document;}
    var dec = RSAencrypt.decrypt(document['EncryptedRandomKey']);
    delete document['EncryptedRandomKey']
    var decryptedContent = CryptoJS.AES.decrypt(JsonFormatter.parse(document['Content']), dec);
    document['Content'] = decryptedContent.toString(CryptoJS.enc.Utf8);
    return document;
}

function returnDocumentToServer(document){
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {if (xhttp.readyState == 4 && xhttp.status == 200) {console.dir('Success!');}};
    xhttp.open("POST", "/depositDocument", true);
    xhttp.setRequestHeader("Content-type", "application/json");
    xhttp.send(JSON.stringify(document));
}

var JsonFormatter = {
        stringify: function (cipherParams) {
            // create json object with ciphertext
            var jsonObj = {
                ct: cipherParams.ciphertext.toString(CryptoJS.enc.Base64)
            };

            // optionally add iv and salt
            if (cipherParams.iv) {
                jsonObj.iv = cipherParams.iv.toString();
            }
            if (cipherParams.salt) {
                jsonObj.s = cipherParams.salt.toString();
            }

            // stringify json object
            return JSON.stringify(jsonObj);
        },

        parse: function (jsonStr) {
            // parse json string
            var jsonObj = JSON.parse(jsonStr);

            // extract ciphertext from json object, and create cipher params object
            var cipherParams = CryptoJS.lib.CipherParams.create({
                ciphertext: CryptoJS.enc.Base64.parse(jsonObj.ct)
            });

            // optionally extract iv and salt
            if (jsonObj.iv) {
                cipherParams.iv = CryptoJS.enc.Hex.parse(jsonObj.iv);
            }
            if (jsonObj.s) {
                cipherParams.salt = CryptoJS.enc.Hex.parse(jsonObj.s);
            }

            return cipherParams;
        }
    };
