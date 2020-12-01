<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:xi="urn:xi" xmlns:css="urn:css">
  <xsl:template match="/">
    <h1><xsl:value-of select="/R/data/limit/@limit"/></h1>
    <table class='tsimple' width='100%'>
      <xsl:for-each select='/R/data/orders/order'>
        <tr>
          <td>
            <xsl:element name='a'>
              <xsl:attribute name='href'>/private/order?order_id=<xsl:value-of select="@order_id"/></xsl:attribute>
              <xsl:attribute name='target'>_blank</xsl:attribute>
              <xsl:value-of select='@order_id'/>
            </xsl:element>
          </td>
          <td>
            <xsl:value-of select="@datetime"/>
          </td>
          <td>
            <xsl:value-of select="@amount"/>
          </td>
        </tr>
      </xsl:for-each>
      <tr><td colspan="2">Итого за указанный период:</td><td><xsl:value-of select="/R/data/orders/all_amount"/></td></tr>
      <tr><td colspan="2">Всего заказов:</td><td><xsl:value-of select="/R/data/count"/></td></tr>
    </table>
  </xsl:template>
</xsl:stylesheet>

