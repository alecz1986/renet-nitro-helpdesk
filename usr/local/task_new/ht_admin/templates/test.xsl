<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:xi="urn:xi" xmlns:css="urn:css">
  <xsl:template match="/">
    <font>Проверьте данные на корректность ввода.</font>
    <br/>
    <table class='tsimple' width='100%'>
      <tr>
        <td>Артикул</td>
        <td>Имя</td>
        <td>Полное описание</td>
        <td>Краткое описание</td>
        <td>Цена</td>
        <td>Старая цена</td>
        <td>Товар недели</td>
        <td>Скидка</td>
        <td>Бонусы</td>
        <td>Спецпредложение</td>
        <td>Доставка</td>
        <td>Тип</td>
        <td>Стол заказов</td>
        <td>Параметры</td>
        <td>Категории</td>
        <td>Видимость</td>
        <td>Товар к НГ</td>
        <td>Единицы измерения</td>
        <td>Ключевые слова</td>
        <td>Дополнительный товары</td>
        <td>Прибыль процент</td>
        <td>Прибыль сумма</td>
      </tr>
      <xsl:for-each select='/R/data/product'>
        <tr>
          <td><xsl:value-of select='@articul'/></td>
          <td><xsl:value-of select='@name'/></td>
          <td><xsl:value-of select='@discription'/></td>
          <td><xsl:value-of select='@overview'/></td>
          <td><xsl:value-of select='@price'/></td>
          <td><xsl:value-of select='@price_old'/></td>
          <td><xsl:value-of select='@week'/></td>
          <td><xsl:value-of select='@sale'/></td>
          <td><xsl:value-of select='@bonus'/></td>
          <td><xsl:value-of select='@spec'/></td>
          <td><xsl:value-of select='@delivery'/></td>
          <td><xsl:value-of select='@vat'/></td>
          <td><xsl:value-of select='@order_desk'/></td>
          <td><xsl:value-of select='@params'/></td>
          <td><xsl:value-of select='@category'/></td>
          <td><xsl:value-of select='@visible'/></td>
          <td><xsl:value-of select='@holiday'/></td>
          <td><xsl:value-of select='@metric'/></td>
          <td><xsl:value-of select='@kw'/></td>
          <td><xsl:value-of select='@complements'/></td>
          <td><xsl:value-of select='@procent'/></td>
          <td><xsl:value-of select='@profit'/></td>
        </tr>
      </xsl:for-each>
    </table>
    <br/>
    <a href='/private/product/download'>Вернуться назад</a>&#160;
    <xsl:element name='a'>
      <xsl:attribute name='href'>?action=commit&#38;distrib_id=<xsl:value-of select="/R/data/@distrib_id"/>&#38;csv=<xsl:value-of select="/R/data/@fname"/>&#38;codding=<xsl:value-of select="/R/data/@codding"/>&#38;separate=<xsl:value-of select="/R/data/@separate"/></xsl:attribute>
        Продолжить дальше загрузку
    </xsl:element>
    <xsl:if test='/R/results/result'>
      <a href='/private/product/zip'>Загрузить фото</a>
    </xsl:if>
  </xsl:template>
</xsl:stylesheet>

