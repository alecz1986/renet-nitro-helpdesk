<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:xi="urn:xi" xmlns:css="urn:css">
  <xsl:template match="/">
    <table class='tsimple' width='100%'>
      <tr><td colspan='4'>Все спецпредложения</td></tr>
      <xsl:for-each select='/R/playlist/trackList/track'>
        <tr>
          <td>
            <xsl:element name='a'>
              <xsl:attribute name='href'><xsl:value-of select='./info'/></xsl:attribute>
              <xsl:value-of select='./info'/>
            </xsl:element>
          </td>
          <td>
            <xsl:element name='img'>
              <xsl:attribute name='src'><xsl:value-of select='./location'/></xsl:attribute>
              <xsl:attribute name='border'>0</xsl:attribute>
            </xsl:element>
          </td>
          <td>
            <xsl:element name='a'>
              <xsl:attribute name='href'>./spec?action=delete&#38;num=<xsl:value-of select='./@num'/></xsl:attribute>
              удалить
            </xsl:element>
          </td>
          <td>
            <xsl:element name='a'>
              <xsl:attribute name='href'>./spec?action=''&#38;num=<xsl:value-of select='./@num'/>&#38;uri=<xsl:value-of select='./info'/></xsl:attribute>
              изменить
            </xsl:element>
          </td>
        </tr>
      </xsl:for-each>
    </table>
    <br/>
    <a href='./spec'>Добавить запись</a>
    <br/>
  </xsl:template>
</xsl:stylesheet>
