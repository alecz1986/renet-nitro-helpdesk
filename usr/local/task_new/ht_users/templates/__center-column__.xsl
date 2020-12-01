<xsl:stylesheet version="1.0" xmlns="http://www.w3.org/1999/xhtml" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:xi="urn:xi" xmlns:css="urn:css">
  <xsl:template match="/">
    <!--<div class='center-column'>-->
        <xi:bind name="banners-top"/>
        <xsl:if test="/R/data/@auto = '1'">
          <!-- форма поиска шин-->
          <xi:bind name="form1"/>
        </xsl:if>
        <xi:bind name="body"/>
        <xi:bind name="body1"/>
        <xi:bind name="menu"/>
        <xi:bind name="form"/>
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
        <!-- </div>-->
  </xsl:template>
</xsl:stylesheet>
