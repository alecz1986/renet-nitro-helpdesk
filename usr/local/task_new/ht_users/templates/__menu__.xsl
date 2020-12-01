<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:xi="urn:xi" xmlns:css="urn:css">
  <xsl:template match="/">
    <br/>
    <table css:border="0">
      <tbody>
        <xsl:for-each select="/R/data/menu">
          <tr>
            <td>
              <li>
                <xsl:element name="a">
                  <xsl:attribute name="href">
                    <xsl:value-of select="./url"/>
                  </xsl:attribute>
                  <xsl:value-of select="./text"/>
                </xsl:element>
                <br/>
                <div class="post_date"> 
                  <xsl:value-of select="./date"/>
                </div>
                <xsl:if test='./photo'>
                  <xsl:element name="img">
                    <xsl:attribute name="src">
                      <xsl:value-of select='/R/page/serv/@name'/><xsl:value-of select="./photo"/>
                    </xsl:attribute>
                    <xsl:attribute name="width">300</xsl:attribute>
                  </xsl:element>
                </xsl:if>
                <br/>
                <font size='3'>
                  <xsl:value-of select="./comment"/>
                </font>
                <br/>
              </li>
            </td>
          </tr>
        </xsl:for-each>
      </tbody>
    </table>
  </xsl:template>
</xsl:stylesheet>
