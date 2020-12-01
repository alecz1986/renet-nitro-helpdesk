<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:xi="urn:xi" xmlns:css="urn:css">
  <xsl:template match="/">
    <table class='tsimple' width='100%'>
      <xsl:for-each select='/R/data/delivery'>
        <tr>
          <td>
            <xsl:element name='a'>
              <xsl:attribute name='href'>./delivery?payment_id=<xsl:value-of select='@payment_id'/>&#38;name=<xsl:value-of select='@name'/>&#38;note=<xsl:value-of select='@note'/>&#38;delivery_id=<xsl:value-of select='@delivery_id'/></xsl:attribute>
              <xsl:value-of select='@name'/>
            </xsl:element>
          </td>
          <td><xsl:value-of select='@note'/></td>
          <td><xsl:value-of select='@payment_name'/></td>
          <td>
            <xsl:element name='a'>
              <xsl:attribute name='href'>./delivery?action=delete&#38;delivery_id=<xsl:value-of select='@delivery_id'/></xsl:attribute>
              удалить
            </xsl:element>
          </td>
        </tr>
      </xsl:for-each>
    </table>
  </xsl:template>
</xsl:stylesheet>

