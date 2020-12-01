<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:xi="urn:xi" xmlns:css="urn:css">
  <xsl:template match="/">
    <table class='tsimple' width='100%'>
      <xsl:for-each select='/R/data/new'>
        <tr>
          <td>
            <xsl:element name='a'>
              <xsl:attribute name='href'>./<xsl:value-of select='/R/data/@link'/>?name=<xsl:value-of select='@name'/>&#38;new_id=<xsl:value-of select='@new_id'/>&#38;overview=<xsl:value-of select='@text'/>&#38;uri=<xsl:value-of select='@uri'/></xsl:attribute>
              <xsl:value-of select='@name'/>
            </xsl:element>
          </td>
          <td><xsl:value-of select='@uri'/></td>
          <td><xsl:value-of select='@text'/></td>
          <td>
            <xsl:element name='img'>
              <xsl:attribute name='src'>/<xsl:value-of select='@photo'/></xsl:attribute>
              <xsl:attribute name='border'>0</xsl:attribute>
            </xsl:element>
          </td>
          <td>
            <xsl:element name='a'>
              <xsl:attribute name='href'>./<xsl:value-of select='/R/data/@link'/>?action=delete&#38;new_id=<xsl:value-of select='@new_id'/></xsl:attribute>
              удалить
            </xsl:element>
          </td>
        </tr>
      </xsl:for-each>
    </table>
    <br/>
    <a href='./new'>Добавить запись</a>
    <br/>
  </xsl:template>
</xsl:stylesheet>

