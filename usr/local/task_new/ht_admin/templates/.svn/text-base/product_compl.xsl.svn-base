<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:xi="urn:xi" xmlns:css="urn:css">
  <xsl:template match="/">
    <table class='tsimple' width='500'>
      <tr><td colspan='2'>Дополнительный товар</td></tr>
      <xsl:for-each select='/R/data/compl'>
        <tr>
          <td>
            <xsl:element name="a">
              <xsl:attribute name="href">./complement?compl_id=<xsl:value-of select='@compl_id'/></xsl:attribute>
              <xsl:value-of select='@art'/>
            </xsl:element>
          </td>
          <td>
            <xsl:element name='a'>
              <xsl:attribute name='href'>./complement?compl_id=<xsl:value-of select='@compl_id'/>&#38;action=del</xsl:attribute>
              удалить
            </xsl:element>
          </td>
        </tr>
      </xsl:for-each>
    </table>
    <br/>
    <xsl:element name='a'>
      <xsl:attribute name='href'>./complement?prod_id=<xsl:value-of select='/R/data/@product_id'/></xsl:attribute>
      добавить новую запись 
    </xsl:element>
  </xsl:template>
</xsl:stylesheet>

