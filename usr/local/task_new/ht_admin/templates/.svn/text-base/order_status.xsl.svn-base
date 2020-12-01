<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:xi="urn:xi" xmlns:css="urn:css">
  <xsl:template match="/">
    <font>Проверьте данные на корректность ввода.</font>
    <br/>
    <table class='tsimple' width='500'>
      <tr><td>Дата</td><td>Статус</td></tr>
      <xsl:for-each select='/R/data/status'>
        <tr>
          <td><xsl:value-of select='@date'/></td>
          <td><xsl:value-of select='@status'/></td>
        </tr>
      </xsl:for-each>
    </table>
  </xsl:template>
</xsl:stylesheet>

