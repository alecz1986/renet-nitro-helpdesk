<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:xi="urn:xi" xmlns:css="urn:css">
  <xsl:template match="/">
    <table class='tsimple' width='500'>
      <tr><td>Название параметра</td><td colspan='2'>Значение</td></tr>
      <xsl:for-each select='/R/data/tehnical'>
        <tr>
          <td><xsl:value-of select='@name'/></td>
          <td><xsl:value-of select='@value'/></td>
          <td>
            <xsl:element name='a'>
              <xsl:attribute name='href'>./tehnical?params=<xsl:value-of select='@id'/>&#38;action='delete'&#38;product_id=<xsl:value-of select='@prod'/></xsl:attribute>
              удалить
            </xsl:element>
          </td>
        </tr>
      </xsl:for-each>
    </table>
  </xsl:template>
</xsl:stylesheet>

