function Menu(k){
   var hrefname = new Array("главная", "аккаунты", "платежи", "платежные системы", "переводы", "генерация аккаунтов", "управление операторами")

   var hrefvalue = new Array( "http://billot.renet.ru/opers_index.cgi", "http://billot.renet.ru/accounts.cgi", "http://billot.renet.ru/opers_payments.cgi", "http://billot.renet.ru/payment_systems.cgi", "http://billot.renet.ru/opers_card_payments.cgi", "http://billot.renet.ru/account_gen.cgi", "http://billot.renet.ru/opers.cgi", "http://billot.renet.ru/payment.cgi?id=1", "http://billot.renet.ru/payment.cgi?id=12")
   var l = hrefvalue.length 
   var Myt = 0
   for (var i = 1; i <= l; i++){
   if (location.href == hrefvalue[i-1])
       {   var Myt = i
       }
   }
   if (Myt<8){ 
   for (var j = 1; j <= k; j++){
         if (j == Myt){
           var parent = document.getElementById('Mytr');
           var myTD = document.createElement("td");
           myTD.setAttribute("width", "100");
           myTD.setAttribute("height", "50");
           myTD.setAttribute("align", "center");
           myTD.setAttribute("valign", "middle");
           myTD.setAttribute("background", "/jpg/15.jpg");
           myTD.setAttribute("id", ""+j);
           myTD.setAttribute("onMouseOver", "ChangeBackGround('"+j+"','/jpg/href_new.jpg')");
           myTD.setAttribute("onMouseOut", "ChangeBackGround('"+j+"','/jpg/15.jpg')");
           parent.appendChild(myTD);
           var myA = document.createElement("a");
           myA.setAttribute("class","hrefjpg");
           myA.setAttribute("style","color: #06126F;");
           myA.setAttribute("href",""+hrefvalue[j-1]);
           myA.appendChild( document.createTextNode( ""+hrefname[j-1]));;
           myTD.appendChild(myA);
              }
        else{
         var parent = document.getElementById('Mytr');
           var myTD = document.createElement("td");
           myTD.setAttribute("width", "100");
           myTD.setAttribute("height", "50");
           myTD.setAttribute("align", "center");
           myTD.setAttribute("valign", "middle");
           myTD.setAttribute("background", "/jpg/href_new.jpg");
           myTD.setAttribute("id", ""+j);
           myTD.setAttribute("onMouseOver", "ChangeBackGround('"+j+"','/jpg/hrefover.jpg')");
           myTD.setAttribute("onMouseOut", "ChangeBackGround('"+j+"','/jpg/href_new.jpg')");
           parent.appendChild(myTD);
           var myA = document.createElement("a");
           myA.setAttribute("class","hrefjpg");
           myA.setAttribute("href",""+hrefvalue[j-1]);
           myA.appendChild( document.createTextNode( ""+hrefname[j-1] ));;
           myTD.appendChild(myA);
       }

      }
}
   else{
     for (var j = 1; j <= k; j++){
          if (j==4){ 
           var parent = document.getElementById('Mytr');
           var myTD = document.createElement("td");
           myTD.setAttribute("width", "100");
           myTD.setAttribute("height", "50");
           myTD.setAttribute("align", "center");
           myTD.setAttribute("valign", "middle");
           myTD.setAttribute("background", "/jpg/15.jpg");
           myTD.setAttribute("id", ""+j);
           myTD.setAttribute("onMouseOver", "ChangeBackGround('"+j+"','/jpg/href.jpg')");
           myTD.setAttribute("onMouseOut", "ChangeBackGround('"+j+"','/jpg/15.jpg')");
           parent.appendChild(myTD);
           var myA = document.createElement("a");
           myA.setAttribute("class","hrefjpg");
           myA.setAttribute("style","color: #06126F;");
           myA.setAttribute("href",""+hrefvalue[j-1]);
           myA.appendChild( document.createTextNode( ""+hrefname[j-1]));;
           myTD.appendChild(myA);
              }
        else{
         var parent = document.getElementById('Mytr');
           var myTD = document.createElement("td");
           myTD.setAttribute("width", "100");
           myTD.setAttribute("height", "50");
           myTD.setAttribute("align", "center");
           myTD.setAttribute("valign", "middle");
           myTD.setAttribute("background", "/jpg/href_new.jpg");
           myTD.setAttribute("id", ""+j);
           myTD.setAttribute("onMouseOver", "ChangeBackGround('"+j+"','/jpg/href.jpg')");
           myTD.setAttribute("onMouseOut", "ChangeBackGround('"+j+"','/jpg/href_new.jpg')");
           parent.appendChild(myTD);
           var myA = document.createElement("a");
           myA.setAttribute("class","hrefjpg");
           myA.setAttribute("href",""+hrefvalue[j-1]);
           myA.appendChild( document.createTextNode( ""+hrefname[j-1] ));;
           myTD.appendChild(myA);
       }

      }
 
}}

