<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:xi="urn:xi" xmlns:css="urn:css">
  <xsl:template match="/">
    <table class='tsimple' width='100%'>
      <xsl:for-each select='/R/data/payment'>
        <tr>
          <td>
            <xsl:element name='a'>
              <xsl:attribute name='href'>./payment?payment_id=<xsl:value-of select='@payment_id'/>&#38;sale_type=<xsl:value-of select='@sale_type'/>&#38;name=<xsl:value-of select='@name'/>&#38;discription=<xsl:value-of select='@discription'/></xsl:attribute>
              <xsl:value-of select='@name'/>
            </xsl:element>
          </td>
          <td><xsl:value-of select='@discription'/></td>
          <td><xsl:value-of select='@sale_type'/></td>
          <td>
            <xsl:element name='a'>
              <xsl:attribute name='href'>./payment?action=delete&#38;payment_id=<xsl:value-of select='@payment_id'/></xsl:attribute>
              удалить
            </xsl:element>
          </td>
        </tr>
      </xsl:for-each>
    </table>
  </xsl:template>
</xsl:stylesheet>

