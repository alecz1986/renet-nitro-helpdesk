<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:xi="urn:xi" xmlns:css="urn:css">
  <xsl:template match="/">
    <table class='tsimple' width='100%'>
      <xsl:for-each select='/R/data/status'>
        <tr>
          <td>
            <xsl:element name='a'>
              <xsl:attribute name='href'>./status?name=<xsl:value-of select='@name'/>&#38;status_id=<xsl:value-of select='@status_id'/></xsl:attribute>
              <xsl:value-of select='@name'/>
            </xsl:element>
          </td>
          <td>
            <xsl:element name='a'>
              <xsl:attribute name='href'>./status?action=delete&#38;status_id=<xsl:value-of select='@status_id'/></xsl:attribute>
              удалить
            </xsl:element>
          </td>
        </tr>
      </xsl:for-each>
    </table>
  </xsl:template>
</xsl:stylesheet>

