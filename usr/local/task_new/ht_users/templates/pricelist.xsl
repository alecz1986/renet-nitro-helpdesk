<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:xi="urn:xi" xmlns:css="urn:css">
  <xsl:template match="/">
    <table class="tsimple" width="100%">
      <xsl:for-each select="/R/data/categorys/category">
        <tr class='top'><td colspan='3' class='no'><b><xsl:value-of select="@name"/></b></td></tr>
        <tr class='top'><td><b>Продукт</b></td><td><b>Цена</b></td><td class='no'><b>Бонусы</b></td></tr>
        <xsl:for-each select="product">
          <tr><td>
              <xsl:element  name='a'>
                <xsl:attribute name='href'>/product?product_id=<xsl:value-of select="@id"/></xsl:attribute>
                <xsl:value-of select="@name"/>
              </xsl:element>
            </td>
            <td class='black'><xsl:value-of select="@price"/></td>
            <td class='no_black'><xsl:value-of select="@bonus"/></td>
          </tr>
        </xsl:for-each>
      </xsl:for-each>
    </table>
  </xsl:template>
</xsl:stylesheet>
