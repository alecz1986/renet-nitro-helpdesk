<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:xi="urn:xi" xmlns:css="urn:css">
  <xsl:template match="/">
    <table class='tsimple' width='100%'>
      <xsl:for-each select='/R/data/suppl'>
        <tr>
          <td>
            <xsl:element name='a'>
              <xsl:attribute name='href'>./supplier?supplier_id=<xsl:value-of select='@supplier_id'/></xsl:attribute>
              <xsl:value-of select='@name'/>
            </xsl:element>
          </td>
          <td><xsl:value-of select='@category_id'/></td>
          <td><xsl:value-of select='@vat'/></td>
          <td><xsl:value-of select='@contact'/></td>
          <td><xsl:value-of select='@phone'/></td>
          <td><xsl:value-of select='@procent'/></td>
          <td><xsl:value-of select='@cct'/></td>
          <td width='200px'>
            <xsl:element name='a'>
              <xsl:attribute name='href'>./supplier?action=delete&#38;supplier_id=<xsl:value-of select='@supplier_id'/></xsl:attribute>
              удалить
            </xsl:element>
          </td>
        </tr>
      </xsl:for-each>
    </table>
    <br/>
    <xsl:element name='a'>
      <xsl:attribute name='href'>./supplier</xsl:attribute>
     Добавить поставщика 
    </xsl:element>
  </xsl:template>
</xsl:stylesheet>

