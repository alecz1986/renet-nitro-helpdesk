var creepingData=new Array();
    creepingData[0]=new Object();
    creepingData[0]={
        'title':'âÉÚÎÅÓ-ëÏÌÌÅÄÖ éòâéó. äÌÑ ÐÏÓÔÕÐÌÅÎÉÑ ÄÏÓÔÁÔÏÞÎÏ ÂÁÚÏ×ÙÈ åçü.ôÅÌ.:39-30-30',
        'link':'http://www.sarbc.ru/advert/goto.php?id=499',
        'color':'#0E06A4',
        'length':'74'
    }
    creepingData[1]=new Object();
    creepingData[1]={
        'title':'ïôëòùôùê ìåôîéê âáóóåêî ÎÁ îÁÂÅÒÅÖÎÏÊ 28-70-79',
        'link':'http://www.sarbc.ru/advert/goto.php?id=503',
        'color':'#0E06A4',
        'length':'46'
    }
    creepingData[2]=new Object();
    creepingData[2]={
        'title':'áÎÇÌÉÊÓËÉÅ ËÁÎÉËÕÌÙ × ÌÁÇÅÒÅ "óÏÓÎÏ×ÙÊ ÂÏÒ"! 24-77-86',
        'link':'http://www.sarbc.ru/advert/goto.php?id=505',
        'color':'#FF0000',
        'length':'53'
    }
    creepingData[3]=new Object();
    creepingData[3]={
        'title':'åçü. 2 ×ÏÌÎÁ. çÏÔÏ×ØÓÑ Ë ÓÄÁÞÅ × ëÏÎÓÕÌØÔÁÔÉ×ÎÏÍ ãÅÎÔÒÅ éòâéó. 39-30-30',
        'link':'http://www.sarbc.ru/advert/goto.php?id=492',
        'color':'#0B794E',
        'length':'71'
    }
    creepingData[4]=new Object();
    creepingData[4]={
        'title':'ïÔËÒÙÔÁ ÎÏ×ÁÑ ÜÌÉÔÎÁÑ ÓÐÅÃÉÁÌØÎÏÓÔØ',
        'link':'http://www.sarbc.ru/advert/goto.php?id=475',
        'color':'#000000',
        'length':'35'
    }
    creepingData[5]=new Object();
    creepingData[5]={
        'title':'èÏÞÅÛØ ÓÔÉÐÅÎÄÉÀ 20.000 ÒÕÂ.? ðÏÓÔÕÐÁÊ × éòâéó! ôÅÌ.: 39-30-30',
        'link':'http://www.sarbc.ru/advert/goto.php?id=493',
        'color':'#FF0000',
        'length':'62'
    }
function creepingUpdater()
{
    creepingStringPos++;
    if (creepingStringPos==1)
    {
        creepingContent.style.color=creepingData[creepingPos].color;
        creepingContent.href=creepingData[creepingPos].link;
    }
    if (creepingStringPos>creepingData[creepingPos].length)
    {
        creepingFinalCounter++;
        if (creepingFinalCounter>35)
        {
            creepingPos++;
            creepingStringPos=0;
            creepingFinalCounter=0;
            if (creepingPos>(creepingData.length-1))
            {
                creepingPos=0;
            }
        }
        else
        {
            creepingStringPos--;
        }
    }
    var creepingString=creepingData[creepingPos].title;
    creepingString=creepingString.substr(0,creepingStringPos);

    creepingSpan.innerHTML=creepingString;
    setTimeout('creepingUpdater()',100);
}

function start(){
//	var c=0;
//	var creepingSpan=document.getElementById('creepingSpan');
//	var creepingContent=document.getElementById('creepingContent');
//	var creepingFinalCounter=0; // ÓÞ£ÔÞÉË ÒÁÂÏÔÁÅÔ ËÏÇÄÁ ÓÔÒÏËÁ ÕÖÅ ÐÏÌÎÏÓÔØÀ ÎÁ ÜËÒÁÎÅ
//	var creepingPos=0; // ÞÔÏ ÉÍÅÎÎÏ ÉÚ creepingData ÃÅÐÌÑÔØ
//	var creepingStringPos=0; // ÐÏÚÉÃÉÑ × ÓÔÒÏËÅ
//	var creepingTimer=null; // ÔÁÊÍÅÒ
	//setInterval('creepingUpdater()',100);
//	creepingUpdater();
	
	$("#site-footer").css("top" , $(document).height()+'px');
	$("#creepingline").css("width" , $(document).width()-500+'px');
	$("#site-footer").css("width" , "95%");
//	$(".week-goods").css("width" , $(document).width()-500);
}
var creepingData=new Array();
    creepingData[0]=new Object();
    creepingData[0]={
        'title':'Ð‘Ð¸Ð·Ð½ÐµÑ-ÐšÐ¾Ð»Ð»ÐµÐ´Ð¶ Ð˜Ð Ð‘Ð˜Ð¡. Ð”Ð»Ñ Ð¿Ð¾ÑÑ‚ÑƒÐ¿Ð»ÐµÐ½Ð¸Ñ Ð´Ð¾ÑÑ‚Ð°Ñ‚Ð¾Ñ‡Ð½Ð¾ Ð±Ð°Ð·Ð¾Ð²Ñ‹Ñ… Ð•Ð“Ð­.Ð¢ÐµÐ».:39-30-30',
        'link':'http://www.sarbc.ru/advert/goto.php?id=499',
        'color':'#0E06A4',
        'length':'74'
    }
    creepingData[1]=new Object();
    creepingData[1]={
        'title':'ÐžÐ¢ÐšÐ Ð«Ð¢Ð«Ð™ Ð›Ð•Ð¢ÐÐ˜Ð™ Ð‘ÐÐ¡Ð¡Ð•Ð™Ð Ð½Ð° ÐÐ°Ð±ÐµÑ€ÐµÐ¶Ð½Ð¾Ð¹ 28-70-79',
        'link':'http://www.sarbc.ru/advert/goto.php?id=503',
        'color':'#0E06A4',
        'length':'46'
    }
    creepingData[2]=new Object();
    creepingData[2]={
        'title':'ÐÐ½Ð³Ð»Ð¸Ð¹ÑÐºÐ¸Ðµ ÐºÐ°Ð½Ð¸ÐºÑƒÐ»Ñ‹ Ð² Ð»Ð°Ð³ÐµÑ€Ðµ "Ð¡Ð¾ÑÐ½Ð¾Ð²Ñ‹Ð¹ Ð±Ð¾Ñ€"! 24-77-86',
        'link':'http://www.sarbc.ru/advert/goto.php?id=505',
        'color':'#FF0000',
        'length':'53'
    }
    creepingData[3]=new Object();
    creepingData[3]={
        'title':'Ð•Ð“Ð­. 2 Ð²Ð¾Ð»Ð½Ð°. Ð“Ð¾Ñ‚Ð¾Ð²ÑŒÑÑ Ðº ÑÐ´Ð°Ñ‡Ðµ Ð² ÐšÐ¾Ð½ÑÑƒÐ»ÑŒÑ‚Ð°Ñ‚Ð¸Ð²Ð½Ð¾Ð¼ Ð¦ÐµÐ½Ñ‚Ñ€Ðµ Ð˜Ð Ð‘Ð˜Ð¡. 39-30-30',
        'link':'http://www.sarbc.ru/advert/goto.php?id=492',
        'color':'#0B794E',
        'length':'71'
    }
    creepingData[4]=new Object();
    creepingData[4]={
        'title':'ÐžÑ‚ÐºÑ€Ñ‹Ñ‚Ð° Ð½Ð¾Ð²Ð°Ñ ÑÐ»Ð¸Ñ‚Ð½Ð°Ñ ÑÐ¿ÐµÑ†Ð¸Ð°Ð»ÑŒÐ½Ð¾ÑÑ‚ÑŒ',
        'link':'http://www.sarbc.ru/advert/goto.php?id=475',
        'color':'#000000',
        'length':'35'
    }
    creepingData[5]=new Object();
    creepingData[5]={
        'title':'Ð¥Ð¾Ñ‡ÐµÑˆÑŒ ÑÑ‚Ð¸Ð¿ÐµÐ½Ð´Ð¸ÑŽ 20.000 Ñ€ÑƒÐ±.? ÐŸÐ¾ÑÑ‚ÑƒÐ¿Ð°Ð¹ Ð² Ð˜Ð Ð‘Ð˜Ð¡! Ð¢ÐµÐ».: 39-30-30',
        'link':'http://www.sarbc.ru/advert/goto.php?id=493',
        'color':'#FF0000',
        'length':'62'
    }

function creepingUpdater()
{
    creepingStringPos++;
    if (creepingStringPos==1)
    {
        creepingContent.style.color=creepingData[creepingPos].color;
        creepingContent.href=creepingData[creepingPos].link;
    }
    if (creepingStringPos>creepingData[creepingPos].length)
    {
        creepingFinalCounter++;
        if (creepingFinalCounter>35)
        {
            creepingPos++;
            creepingStringPos=0;
            creepingFinalCounter=0;
            if (creepingPos>(creepingData.length-1))
            {
                creepingPos=0;
            }
        }
        else
        {
            creepingStringPos--;
        }
    }
    var creepingString=creepingData[creepingPos].title;
    creepingString=creepingString.substr(0,creepingStringPos);

    creepingSpan.innerHTML=creepingString;
    setTimeout('creepingUpdater()',100);
}


