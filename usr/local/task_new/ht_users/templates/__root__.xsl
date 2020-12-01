<xsl:stylesheet version="1.0" xmlns="http://www.w3.org/1999/xhtml" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:xi="urn:xi" xmlns:css="urn:css">
  <xsl:output method="xml"/>
  <xsl:template match="/">
<html>
  <head>
    <meta http-equiv="Content-Type" content="text/html;charset=utf-8" />
    <title id="page.title"><xsl:value-of select="/R/page/title"/></title>
    <script type="text/javascript" src="/js/jquery-1.2.6.js"></script>
    <xsl:for-each select="/R/external/*">
      <xsl:call-template name="external"/>
    </xsl:for-each>
    <link rel="STYLESHEET"   href="/css/style_admin.css"/>
    <script type="text/javascript" src="/js/calendar.js"></script>
    <script type="text/javascript" src="/js/calendar-ru.js"></script>
    <script type="text/javascript" src="/js/calendar-setup.js"></script>
  </head>
  <body css:font-size="0.8em" css:font-family="Arial,Verdana,Helvetica,sans-serif" css:background-color="white" css:margin="0px 0px 0px 0px">
    <table border="0" cellpadding="1" cellspacing="1" align="center" width="90%">
      <xsl:element name="tr">
        <xsl:attribute name="bgcolor"><xsl:value-of select="/R/page/main/bgcolor"/></xsl:attribute>
        <td>
          <xsl:for-each select="/R/page/main/menu">
            <xsl:element name="a">
              <xsl:attribute name="href"><xsl:value-of select="./href"/></xsl:attribute>
              <xsl:attribute name="css:color"><xsl:value-of select="./color"/></xsl:attribute>
              <xsl:attribute name="css:padding">3px</xsl:attribute>
              <xsl:value-of select="./name"/>
            </xsl:element>
          </xsl:for-each>
        </td>
        <td align="right" width="150px">
          <xsl:element name="a">
            <xsl:attribute name="href"><xsl:value-of select="/R/page/main/link/href"/></xsl:attribute>
            <xsl:attribute name="css:color"><xsl:value-of select="/R/page/main/link/color"/></xsl:attribute>
            <xsl:attribute name="css:padding">3px</xsl:attribute>
            <xsl:value-of select="/R/page/main/link/name"/>
          </xsl:element>
        </td>
      </xsl:element>
      <tr>
        <td colspan="2" align="center">
           <xsl:if test="/R/user/fio">
             <b>Вы зашли как <xsl:value-of select="/R/user/fio"/>.</b>
           </xsl:if>
           <br/>
           <pre css:color="red">
             <xsl:value-of select="/R/data/inst"/>
           </pre>
           <xsl:if test="/R/data/form1">
             <xi:bind name="form1"/>
           </xsl:if>
           <br/>
           <xi:bind name="body"/>
           <br/>
           <xsl:if test="not(/R/data/@do)">
             <xi:bind name="form"/>
           </xsl:if>
           <xsl:if test="/R/data/@do='1'">
             <xi:bind name="form"/>
           </xsl:if>
           <xsl:if test="/R/errors/error | /R/results/result">
             <table class="menu">
               <tbody>
                 <xsl:for-each select="/R/errors/error">
                   <tr><td><div css:color="red"><xsl:value-of select="."/></div></td></tr>
                 </xsl:for-each>
                 <xsl:for-each select="/R/results/result">
                   <tr><td><div css:color="blue"><xsl:value-of select="."/></div></td></tr>
                 </xsl:for-each>
               </tbody>
             </table>
             <br/>
           </xsl:if>
        </td>
      </tr>
    </table>
  </body>
</html>
  </xsl:template>
  <xsl:template name="external">
    <xsl:choose>
      <xsl:when test="name()='js'">
        <xsl:element name="script">
          <xsl:attribute name="type">text/javascript</xsl:attribute>
          <xsl:attribute name="src"><xsl:value-of select="./text()"/></xsl:attribute>
        </xsl:element>
      </xsl:when>
      <xsl:when test="name()='css'">
        <xsl:element name="link">
          <xsl:attribute name="rel">stylesheet</xsl:attribute>
          <xsl:attribute name="type">text/css</xsl:attribute>
          <xsl:attribute name="href"><xsl:value-of select="./text()"/></xsl:attribute>
        </xsl:element>
      </xsl:when>
      <xsl:otherwise>
      </xsl:otherwise>
    </xsl:choose>
  </xsl:template>
</xsl:stylesheet>
