<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:xi="urn:xi" xmlns:css="urn:css">
  <xsl:template match="/">
    <table class='tsimple' width='100%'>
      <xsl:for-each select='/R/data/delivery'>
        <tr>
          <td>
            <xsl:element name='a'>
              <xsl:attribute name='href'>./price_delivery?name=<xsl:value-of select='@name'/>&#38;price=<xsl:value-of select='@price'/>&#38;delivery_id=<xsl:value-of select='@delivery_id'/></xsl:attribute>
              <xsl:value-of select='@name'/>
            </xsl:element>
          </td>
          <td><xsl:value-of select='@price'/></td>
          <td>
            <xsl:element name='a'>
              <xsl:attribute name='href'>./price_delivery?action=delete&#38;delivery_id=<xsl:value-of select='@delivery_id'/></xsl:attribute>
              удалить
            </xsl:element>
          </td>
        </tr>
      </xsl:for-each>
    </table>
  </xsl:template>
</xsl:stylesheet>

