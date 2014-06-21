/**
 * Created by murad on 24.03.14.
 */

$(document).ready(function (e) {

    var BASE_URL = "/";

    var TIMEOUT = 3000;

    var GLOBAL_OPTIONS = {
        query: "",
        start_width: false,
        sort_by_name: true
    };

    var MESSAGE = {
        wait: "Загрузка...",
        error: "Ошибка: "
    };

    kendo.culture("ru-RU");

    $('.btn-toggle').click(function() {
        $(this).find('.btn').toggleClass('active');

        if ($(this).find('.btn-primary').size()>0) {
            $(this).find('.btn').toggleClass('btn-primary');
        }

        $(this).find('.btn').toggleClass('btn-default');

        GLOBAL_OPTIONS.sort_by_name = !(GLOBAL_OPTIONS.sort_by_name);
        console.log(GLOBAL_OPTIONS.sort_by_name );
        pager.page(1);
    });

    $("#logout").click(function () {
        document.location.href='/logout/';
    });

    var project = $("#products").kendoDropDownList({
        dataSource: {
            type: "json",
            transport: {
                read: {
                    url: BASE_URL + "term/get_projects/",
                    dataType: "json",
                    type: "POST"
                }
            }
        },
        dataTextField: "name",
        dataValueField: "id",
        optionLabel: "Все проекты",
        change: function () {
            GLOBAL_OPTIONS.query = "";
            GLOBAL_OPTIONS.start_width = false;
            search_query.dataSource.read();
            title_render();
            pager.page(1);
            //terms_data_source.read();
        }
    }).data("kendoDropDownList");

    function title_render() {
        var pr = project.value();
        $.post(BASE_URL + "get_titles/", {project: pr} ,function (data) {
            var index = $("#index");
            index.empty();
            if (data.items.length > 0) {
                $.each(data.items, function (i, o) {
                    index.append(
                        '<a class="letter" title="Слова на букву '+o+'">'+o+'</a>'
                    )
                });
            } else {
//                index.append(
//                    '<a href="http://google.com" title="но я могу предложить кое-что другое">Извините, мне нечего вам показать</a>'
//                )
            }
        }, "json").fail(function (data) {
            noti({title: MESSAGE.error + data.status, message: data.statusText}, "error", TIMEOUT);
        });
    }
    title_render();
    var terms_data_source = new kendo.data.DataSource({
        type: "json",
        transport: {
            read: {
                url: BASE_URL + "term/read/",
                dataType: "json",
                type: "POST"
            },
            parameterMap: function (options, operation) {
                if (operation == "read") {
                    var o = {
                        take: options.take,
                        skip: options.skip,
                        query: GLOBAL_OPTIONS.query,
                        start_width: GLOBAL_OPTIONS.start_width,
                        sort_by_name: GLOBAL_OPTIONS.sort_by_name,
                        project: project.value()
                    };
                    return {options: kendo.stringify(o)};
                }
            }
        },
        pageSize: 15,
        serverPaging: true,
        schema: {
            data: "items",
            total: "total"
        }
    });

    var pager = $("#pager").kendoPager({
        dataSource: terms_data_source,
        messages: {
            display: "Записей в списке: {2}",
            empty: "Нет данных для представления",
            first: "Первая страница",
            itemsPerPage: "записей на странице",
            last: "Последняя страница",
            next: "Следующая страница",
            of: "из {0}",
            page: "Страница",
            previous: "Предыдущая страница",
            refresh: "Обновить"
        }
    }).data("kendoPager");

    pager.bind("change", function (e) {

    });

    var terms = $("#terms").kendoListView({
        dataSource: terms_data_source,
        dataBound: function(e) {
            if(this.dataSource.data().length == 0){
                $("<div/>")
                    .attr("class", "term_item")
                    .css("text-align", "center")
                    .append("<h1>Нет данных для представления</h1>")
                    .appendTo("#terms");
            }
        },
        template: kendo.template($("#term_template").html())
    }).data("kendoListView");

    //--------------------------------------------------------------------//

    var search_query = $("#search_form input").kendoAutoComplete({
        dataSource: {
//                serverFiltering: true,
            transport: {
                read: {
                    dataType: "json",
                    type: "POST",
                    url: BASE_URL + "search_suggestions/" ///поисковые подсказки, при вводе в строку поиска
                },
                parameterMap: function (options, operation) {
                    if (operation == "read") {
                        return {project: project.value()};
                    }
                }
            }
        },
        filter: "contains"
//            placeholder: "Поиск",
    }).data("kendoAutoComplete");

    $("#search_form").submit(function(e) { // Поис в форме по совпадению
        GLOBAL_OPTIONS.query = search_query.value();
        GLOBAL_OPTIONS.start_width = false;
        pager.page(1);
        //terms_data_source.read();
        return false;
    });

    $("#index").on("click", ".letter", function(e) { //Поиск по индесу по первой букве
        GLOBAL_OPTIONS.query = $(this).text();
        GLOBAL_OPTIONS.start_width = true;
        pager.page(1);
        //terms_data_source.read();
        return false;
    });

    $(".navbar-brand").click(function(e) {
        GLOBAL_OPTIONS.query = "";
        GLOBAL_OPTIONS.start_width = false;
        pager.page(1);
        //terms_data_source.read();
        return false;
    });

    var term_model = kendo.observable({
        is_edit: false,
        projects: "",
        o: {
            id: 0,
            title: "",
            description: "",
            project: ""
        }
    });
    kendo.bind("#change_term", term_model);
    var term_validator = $("#change_term").kendoValidator({
        rules: {
            required: function (input) {
                if (input.is("[required]")) {
                    input.val($.trim(input.val())); //удалить обертывающиепробелы
                    return input.val() !== "";
                } else return true;
            }
        },
        messages: {
            required: "Поле не может быть пустым"
        }
    }).data("kendoValidator");
    var change_term_window = $("#change_term_window");

    $(".add_term").click(function () {
        $(".k-widget.k-tooltip.k-tooltip-validation.k-invalid-msg").hide();
        term_model.set("is_edit", false);
        term_model.set("projects", project.dataSource.data());
        term_model.set("o", {
            id: 0,
            title: "",
            description: "",
            project: ""
        });
        change_term_window.modal("show");
    });

    function term_response_handler(response) {
        console.log(response);
        var data = terms_data_source.get(response.id);
        if (data) {
            data.title = response.title;
            data.description = response.description;
            data.project = response.project_id;
        } else {
            terms_data_source.insert(0, response);
        }
        noti();
        project.dataSource.read();
        terms.refresh();
        title_render();
        change_term_window.modal("hide");
    }

    $("#term_save").click(function () {
        if (!term_validator.validate()) return false;
        var send = term_model.get("o");
        noti({message: MESSAGE.wait}, "wait");
        $.post("term/" + (term_model.get("is_edit") ? "update/" : "create/"),
            { item: JSON.stringify(send) }, term_response_handler, "json").fail(function (data) {
                noti({title: MESSAGE.error + data.status, message: data.statusText}, "error", TIMEOUT);
            });
        return false;
    });

    $("#terms").on("click", ".edit_term", function (e) {
        var that = $(this);
        var uid = that.closest(".term_item").data("uid");
        var dataItem = terms_data_source.getByUid(uid);
        if (dataItem) {
            $(".k-widget.k-tooltip.k-tooltip-validation.k-invalid-msg").hide();
            term_model.set("is_edit", true);
            term_model.set("projects", project.dataSource.data());
            term_model.set("o", {
                id: dataItem.id,
                title: dataItem.title,
                description: dataItem.description,
                project: dataItem.project_id
            });
            change_term_window.modal("show");
        }
        return false;
    });

    $("#terms").on("click", ".remove_term", function (e) {
        if (!confirm("Вы точно хотите удалить запись?")) return false;
        var that = $(this);
        var uid = that.closest(".term_item").data("uid");
        var dataItem = terms_data_source.getByUid(uid);
        if (dataItem) {
            var send = { id: dataItem.id };
            $.post("term/remove/", { item: JSON.stringify(send) }, function (data) {
                terms_data_source.remove(dataItem);
                title_render();
            }, "json").fail(function (data) {
                noti({title: MESSAGE.error + data.status, message: data.statusText}, "error", TIMEOUT);
            });
        }
        return false;
    });

});