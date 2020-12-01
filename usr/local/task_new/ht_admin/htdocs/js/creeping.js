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
