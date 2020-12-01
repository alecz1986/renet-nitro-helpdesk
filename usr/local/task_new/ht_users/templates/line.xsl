<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:xi="urn:xi" xmlns:css="urn:css">
  <xsl:template match="/">
<html>
<head>
<title></title>
<style type="text/css"> 
body
{
    margin: 0;
    padding:0;
}
 
#creepingContent
{
    display:block;
    font-family:Verdana;
    color:#000000;
    font-size:12px;
    font-weight:bold;
    line-height:20px;
    line-height:18px;
    width:600px;
    height:20px;
    text-decoration:none;
}    
#creepingSpan{display:inline;}
</style>
<script type="text/javascript" src="/js/creeping.js"></script>
</head>
<body css:background-color="#ffffff">
<a href='' target="_blank" id='creepingContent' css:color='#000000'><span id='creepingSpan'></span></a>
<script type="text/javascript"> 
  var creepingData=new Array();
  <xsl:for-each select='/R/data/line'>
    creepingData[<xsl:value-of select='@count'/>]=new Object();
    creepingData[<xsl:value-of select='@count'/>]={
    'title':'<xsl:value-of select='@name'/>',
    'link':'<xsl:value-of select='@link'/>',
    'color':'<xsl:value-of select='@color'/>',
    'length':'<xsl:value-of select='@len'/>'
    }
  </xsl:for-each>
var c=0;
var creepingSpan=document.getElementById('creepingSpan');
var creepingContent=document.getElementById('creepingContent');
var creepingFinalCounter=0;
var creepingPos=0;
var creepingStringPos=0;
var creepingTimer=null;
//setInterval('creepingUpdater()',100);
creepingUpdater();
</script>
</body>
</html>
</xsl:template>
</xsl:stylesheet>
