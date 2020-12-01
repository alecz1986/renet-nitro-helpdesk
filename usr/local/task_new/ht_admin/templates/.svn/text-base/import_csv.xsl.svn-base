<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:xi="urn:xi" xmlns:css="urn:css">
  <xsl:template match="/">
    <br/>
    <div>
      <font color='red' size='3'>
        Уважаемые пользователи!<br/>
        Появились новые поля прибыли.
      </font>
      <br/>
      <br/>
      <br/>
      <font color='red'>Информация по составлению csv-файла</font><br/>
      <pre>
        Для успешной загрузки данных, необходимо следовать следующим пунктам:
        1) таблица продкутов должна содержать заголовки:
            -articul (артикул товара),
            -name (название продукта),
            -overview (краткое описание),
            -discription (детальное описание),
            -delivery (группа стоимости доставки, для просмотра номера соовтетсвующей группа нажмите на <div id="show_delivery" css:color="#0000ff;" css:text-decoration="underline;"><font>Доставка</font></div> ),
            -vat (отношение к НДС (для палтельщиков НДС - "yes",для неплательщиков НДС - "no", все остальные - "all")),
            -sale (скидка есть - "yes", скидки нет - "no"),
            -week (товар недели ("yes", "no")),
            -order_desk (стол заказов (0(нет), 1(да))),
            -bonus (количество бонусов, начисляемых при покупке),
            -spec (спец. предлажение(yes,no)),
            -price (цена),
            -price_old (старая цена),
            -params (характеристики товара. Должны иметь формат название_параметра:значение | название_параметра:значение.),
            -category (Перечнь номеров катеогрий, в которых будет показываться данный товарб  для просмотра номера соовтетсвующей категории нажмите на <div id="show_category" css:color="#0000ff;" css:text-decoration="underline;"><font>Категории</font></div>).
            -visible (Видимость товара. Допустимые значения: <div css:color="red">open</div>, <div css:color="red">close</div>)
            -holiday (Товар к НГ. Допустимые значения: <div css:color="red">yes</div>, <div css:color="red">no</div>)
            -metric (Единицы измерения.)
            -kw (Ключевые слова к продукту, перечисленные через пробел. Ипользуются для оптимизации поиска. Поле работает в режиме дополнения.)
            -complements (Список идентификаторов товаров, перечисленных через запятую. Служит для связи товара с товарами-комплементами (взаимодополняемыми товарами))
            -procent (Прибыль в процентах от стоимости единицы товара)
            -profit (Сумма прибыли с единицы товара)
         2) При отсутсвии одного из полей или его другом именовании загрузка производиться не будет. Порядок следования полей значенгие не имеет.
       </pre>
       <font color='red'>ПРИМЕР</font><br/>
       <table border='1' width='100%' cellspacing='0' callpadding='0'>
         <tr>
           <td>articul</td>
           <td>name</td>
           <td>overview</td>
           <td>discription</td>
           <td>delivery</td>
           <td>vat</td>
           <td>sale</td>
           <td>week</td>
           <td>order_desk</td>
           <td>bonus</td>
           <td>spec</td>
           <td>price</td>
           <td>price_old</td>
           <td>params</td>
           <td>category</td>
           <td>visible</td>
           <td>holiday</td>
           <td>metric</td>
           <td>kw</td>
           <td>complements</td>
           <td>procent</td>
           <td>profit</td>
         </tr>
         <tr>
          <td>10</td>
          <td>продукт10</td>
          <td>краткое описание</td>
          <td>детальное описание</td>
          <td>3</td>
          <td>all</td>
          <td>no</td>
          <td>yes</td>
          <td>0</td>
          <td>1</td>
          <td>yes</td>
          <td>350.00</td>
          <td>0.00</td>
          <td> ширина:150,5 | высота:80</td>
          <td>3,7,5</td>
          <td>open</td>
          <td>no</td>
          <td>шт.</td>
          <td>автобокс багажники</td>
          <td>1, 2, 3</td>
          <td>10.5</td>
          <td>0</td>
         </tr>
      </table>
    </div>
    <a href='/private/product/zip'>Перейти к загрузке фотографий</a>
  </xsl:template>
</xsl:stylesheet>

