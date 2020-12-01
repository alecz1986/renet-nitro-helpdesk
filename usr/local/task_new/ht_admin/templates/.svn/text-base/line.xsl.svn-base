<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:xi="urn:xi" xmlns:css="urn:css">
  <xsl:template match="/">
    <table class='tsimple' width='100%'>
      <xsl:for-each select='/R/data/lines/line'>
        <tr>
          <td>
            <xsl:element name='a'>
              <xsl:attribute name='href'>./line?line_id=<xsl:value-of select='@line_id'/></xsl:attribute>
              <xsl:attribute name='css:color'><xsl:value-of select='@color'/></xsl:attribute>
              <xsl:value-of select='@name'/>
            </xsl:element>
          </td>
          <td><xsl:value-of select='@link'/></td>
          <td>
            <xsl:element name='a'>
              <xsl:attribute name='href'>./line?action=delete&#38;line_id=<xsl:value-of select='@line_id'/></xsl:attribute>
              удалить
            </xsl:element>
          </td>
        </tr>
      </xsl:for-each>
    </table>
    <br/>
    <xsl:element name='a'>
      <xsl:attribute name='href'>./line</xsl:attribute>
     Добавить ссылку
   </xsl:element>
   <br/>
   <img src='/data/colors.gif' border='0px'/>
  </xsl:template>
</xsl:stylesheet>

