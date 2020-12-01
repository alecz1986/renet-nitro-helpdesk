<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:xi="urn:xi" xmlns:css="urn:css">
  <xsl:template match="/">
    <table class='tsimple' width='100%'>
      <xsl:for-each select='/R/data/category'>
        <tr>
          <td>
            <xsl:element name='a'>
              <xsl:attribute name='href'>./category_link?&#38;category_link_id=<xsl:value-of select='@id'/></xsl:attribute>
              <xsl:value-of select='@name'/>
            </xsl:element>
          </td>
          <td><xsl:value-of select='@link'/></td>
          <td>
            <xsl:element name='a'>
              <xsl:attribute name='href'>./category_link?action=delete&#38;category_link_id=<xsl:value-of select='@id'/></xsl:attribute>
              удалить
            </xsl:element>
          </td>
        </tr>
      </xsl:for-each>
    </table>
    <br/>
    <xsl:element name='a'>
      <xsl:attribute name='href'>./category_link?action=&#38;category_id=<xsl:value-of select='/R/data/@category_id'/>&#38;category_link_id=0</xsl:attribute>
     Добавить ссылку
    </xsl:element>
  </xsl:template>
</xsl:stylesheet>

