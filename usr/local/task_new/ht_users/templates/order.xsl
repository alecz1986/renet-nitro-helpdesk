<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:xi="urn:xi" xmlns:css="urn:css">
  <xsl:template match="/">
    <table cellspacing ='0' cellpadding='0' class='tsimple' width='100%'>
      <tr class='top'><td>Продукт</td><td>Стоимость</td><td>Количество</td><td class='no'>Бонусы к оплате</td></tr>
      <xsl:for-each select="/R/data/order/prods/prod">
          <tr>
            <td>
                <xsl:value-of select='@name'/>
            </td>
            <td class='black'><xsl:value-of select='@amount'/></td>
            <td class='black'><xsl:value-of select='@count'/></td>
            <td class='no_black'><xsl:value-of select='@bonus'/></td>
          </tr>
        </xsl:for-each>
      </table>
      <a href='/public/userorder'>Назад к заказам </a>
    </xsl:template>
</xsl:stylesheet>

