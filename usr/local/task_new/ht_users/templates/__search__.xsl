<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:xi="urn:xi" xmlns:css="urn:css">
 <xsl:template match="/">
   <form class='search' action="/searchstring" method="get">
     <xsl:element name="input">
       <xsl:attribute name="class">input</xsl:attribute>
       <xsl:attribute name="type">text</xsl:attribute>
       <xsl:attribute name="name">s</xsl:attribute>
       <xsl:attribute name="value">
         <xsl:choose>
           <xsl:when test="/R/data/@s"> 
             <xsl:value-of select="/R/data/@s"/>
           </xsl:when>
           <xsl:otherwise>
             <xsl:text>поиск</xsl:text>
           </xsl:otherwise>
         </xsl:choose>
       </xsl:attribute>
     </xsl:element>
     <xsl:element name="input">
       <xsl:attribute name="class">submit</xsl:attribute>
       <xsl:attribute name="type">submit</xsl:attribute>
       <xsl:attribute name="value">OK</xsl:attribute>
     </xsl:element>
   </form>
 </xsl:template>
</xsl:stylesheet>
