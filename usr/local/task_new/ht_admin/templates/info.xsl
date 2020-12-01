<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:xi="urn:xi" xmlns:css="urn:css">
  <xsl:template match="/">
    <table class='tsimple' width='100%'>
      <xsl:for-each select='/R/data/info'>
        <tr>
          <td>
            <xsl:element name='a'>
              <xsl:attribute name='href'>./info?name=<xsl:value-of select='@name'/>&#38;action=&#38;info_page_id=<xsl:value-of select='@info_page_id'/>&#38;category_id=<xsl:value-of select='@category_id'/>&#38;uri=<xsl:value-of select='@uri'/></xsl:attribute>
              <xsl:value-of select='@name'/>
            </xsl:element>
          </td>
          <td><xsl:value-of select='@uri'/></td>
          <td><xsl:value-of select='@weight'/></td>

          <td>
            <xsl:element name='a'>
              <xsl:attribute name='href'>./info?action=delete&#38;info_page_id=<xsl:value-of select='@info_page_id'/></xsl:attribute>
              удалить
            </xsl:element>
          </td>
        </tr>
      </xsl:for-each>
    </table>
    <br/>
    <a href='./info'>Добавить запись</a>
    <br/>
  </xsl:template>
</xsl:stylesheet>

