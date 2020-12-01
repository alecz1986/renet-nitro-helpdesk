<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:xi="urn:xi" xmlns:css="urn:css">
  <xsl:template match="/">
    <table class='tsimple' width='100%'>
      <xsl:for-each select='/R/data/banner'>
        <tr>
          <td>
            <xsl:element name='a'>
              <xsl:attribute name='href'>./banners?name=<xsl:value-of select='@name'/>&#38;banner_id=<xsl:value-of select='@banner_id'/>&#38;alt=<xsl:value-of select='@alt'/>&#38;title=<xsl:value-of select='@title'/>&#38;link=<xsl:value-of select='@link'/>&#38;mark=<xsl:value-of select='@mark'/></xsl:attribute>
              <xsl:value-of select='@name'/>
            </xsl:element>
          </td>
          <td><xsl:value-of select='@alt'/></td>
          <td><xsl:value-of select='@title'/></td>
          <td><xsl:value-of select='@link'/></td>
          <td>
            <xsl:element name='a'>
              <xsl:attribute name='href'>./banners?action=delete&#38;banner_id=<xsl:value-of select='@banner_id'/></xsl:attribute>
              удалить
            </xsl:element>
          </td>
        </tr>
      </xsl:for-each>
    </table>
  </xsl:template>
</xsl:stylesheet>

