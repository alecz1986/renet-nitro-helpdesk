<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:xi="urn:xi" xmlns:css="urn:css">
  <xsl:template match="/">
    <br/>
    <xsl:if test="/R/menus/menu">
      <table css:border="0">
        <tbody>
          <xsl:for-each select="/R/menus/menu">
            <tr>
              <td>
                <li>
                  <xsl:element name="a">
                    <xsl:attribute name="href">
                      <xsl:value-of select="./url"/>
                    </xsl:attribute>
                    <xsl:value-of select="./text"/>
                  </xsl:element>
                </li>
              </td>
            </tr>
          </xsl:for-each>
        </tbody>
      </table>
    </xsl:if>
  </xsl:template>
</xsl:stylesheet>
