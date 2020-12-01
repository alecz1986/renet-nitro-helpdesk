<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:xi="urn:xi" xmlns:css="urn:css">
  <xsl:template match="/">
    <div id="show_category" css:color="#0000ff;" css:text-decoration="underline;"><font>Категории</font></div><br/>
    <table class='tsimple' width='500'>
      <tr><td colspan='2'>Категория</td></tr>
      <xsl:for-each select='/R/data/category'>
        <tr>
          <td><xsl:value-of select='@name'/></td>
          <td>
            <xsl:element name='a'>
              <xsl:attribute name='href'>./category?params=<xsl:value-of select='@id'/>&#38;action='delete'&#38;product_id=<xsl:value-of select='@prod'/></xsl:attribute>
              удалить
            </xsl:element>
          </td>
        </tr>
      </xsl:for-each>
    </table>
  </xsl:template>
</xsl:stylesheet>

