/**
 * JavaScript để sửa vấn đề thêm sản phẩm trong form nhập kho
 */

// Đảm bảo jQuery đã sẵn sàng
jQuery(document).ready(function($) {
    // Định nghĩa một hàm để thêm sản phẩm mới
    function addNewProductRow() {
        console.log("Thêm sản phẩm mới vào phiếu nhập kho");

        // Lấy formCount hiện tại từ TOTAL_FORMS
        let formCount = parseInt($('#id_items-TOTAL_FORMS').val() || '0');
        console.log("Số lượng form hiện tại:", formCount);

        // Tạo một dòng mới
        const newRow = $('<tr class="item-row"></tr>');

        // Tạo ô cho sản phẩm (cột 1)
        const productCell = $('<td></td>');
        const productSelect = $('<select class="form-control select2 product-select"></select>');
        productSelect.attr({
            'name': `items-${formCount}-product`,
            'id': `id_items-${formCount}-product`
        });
        // Thêm option mặc định
        productSelect.append('<option value="">-- Chọn sản phẩm --</option>');
        
        // Sao chép tất cả các option từ dropdown đầu tiên nếu có
        const firstSelect = $('.product-select').first();
        if (firstSelect.length > 0) {
            firstSelect.find('option').each(function() {
                if ($(this).val() !== '') {
                    productSelect.append($(this).clone());
                }
            });
        }
        productCell.append(productSelect);
        newRow.append(productCell);

        // Tạo ô cho số lượng hiện tại (cột 2)
        const currentQtyCell = $('<td></td>');
        const currentQtyInput = $('<input type="text" class="form-control" readonly>');
        currentQtyInput.attr({
            'name': `items-${formCount}-current_quantity`,
            'id': `id_items-${formCount}-current_quantity`
        });
        currentQtyCell.append(currentQtyInput);
        newRow.append(currentQtyCell);

        // Tạo ô cho số lượng nhập (cột 3)
        const qtyCell = $('<td></td>');
        const qtyInput = $('<input type="number" class="form-control" min="1" value="1">');
        qtyInput.attr({
            'name': `items-${formCount}-quantity`,
            'id': `id_items-${formCount}-quantity`
        });
        qtyCell.append(qtyInput);
        newRow.append(qtyCell);

        // Tạo ô cho ghi chú (cột 4)
        const notesCell = $('<td></td>');
        const notesInput = $('<input type="text" class="form-control">');
        notesInput.attr({
            'name': `items-${formCount}-notes`,
            'id': `id_items-${formCount}-notes`
        });
        notesCell.append(notesInput);
        newRow.append(notesCell);

        // Tạo ô cho nút xóa (cột 5)
        const deleteCell = $('<td></td>');
        const deleteBtn = $('<button type="button" class="btn btn-danger btn-sm remove-row"><i class="fas fa-trash"></i></button>');
        deleteCell.append(deleteBtn);
        newRow.append(deleteCell);

        // Thêm dòng mới vào bảng
        $('#item-rows').append(newRow);
        console.log(`Đã thêm dòng mới với ${newRow.find('td').length} ô`);

        // Cập nhật form count
        formCount++;
        $('#id_items-TOTAL_FORMS').val(formCount);
        console.log("Đã cập nhật TOTAL_FORMS:", formCount);

        // Khởi tạo select2 cho dropdown mới
        try {
            productSelect.select2({
                theme: 'bootstrap4',
                width: '100%'
            });
            console.log("Đã khởi tạo select2 cho dropdown mới");
        } catch (e) {
            console.error("Lỗi khi khởi tạo select2:", e);
        }

        // Tự động mở dropdown để chọn sản phẩm
        setTimeout(() => {
            try {
                productSelect.select2('open');
            } catch(e) {
                console.warn("Không thể mở dropdown select2:", e);
            }
        }, 100);
        
        return newRow;
    }

    // Gắn sự kiện cho nút thêm sản phẩm (bằng cách override lại)
    console.log("Ghi đè lại chức năng thêm sản phẩm");
    $('#add-row').off('click').on('click', function(e) {
        e.preventDefault();
        e.stopPropagation();
        console.log("Nút thêm sản phẩm được nhấp");
        addNewProductRow();
    });

    // Gắn sự kiện cho nút xóa sản phẩm
    $(document).on('click', '.remove-row', function() {
        if ($('.item-row').length > 1) {
            $(this).closest('tr').remove();
            
            // Cập nhật lại index các form
            $('.item-row').each(function(idx) {
                $(this).find(':input').each(function() {
                    var name = $(this).attr('name');
                    if (name) {
                        var newName = name.replace(/items-\d+/, 'items-' + idx);
                        $(this).attr('name', newName).attr('id', 'id_' + newName);
                    }
                });
            });
            
            // Cập nhật TOTAL_FORMS
            $('#id_items-TOTAL_FORMS').val($('.item-row').length);
        } else {
            alert('Phải có ít nhất một sản phẩm trong phiếu nhập kho');
        }
    });

    // Gắn sự kiện cho select sản phẩm
    $(document).on('change', '.product-select', function() {
        const row = $(this).closest('tr');
        const selectedOption = $(this).find('option:selected');
        
        if (selectedOption.val()) {
            // Lấy thông tin số lượng hiện tại nếu có
            const currentQty = selectedOption.data('current-quantity') || 0;
            row.find('input[name$="-current_quantity"]').val(currentQty);
        } else {
            row.find('input[name$="-current_quantity"]').val('');
            row.find('input[name$="-quantity"]').val('');
        }
    });

    console.log("Đã áp dụng các bản sửa lỗi cho form nhập kho!");
});

// Thêm hiệu ứng CSS cho nút thêm sản phẩm để làm nổi bật
document.addEventListener("DOMContentLoaded", function() {
    const addButton = document.getElementById('add-row');
    if (addButton) {
        addButton.classList.add('btn-pulse');
        
        // Thêm style cho nút
        const style = document.createElement('style');
        style.innerHTML = `
            .btn-pulse {
                animation: pulse 2s infinite;
                box-shadow: 0 0 0 rgba(23, 162, 184, 0.4);
            }
            
            @keyframes pulse {
                0% {
                    box-shadow: 0 0 0 0 rgba(23, 162, 184, 0.4);
                }
                70% {
                    box-shadow: 0 0 0 10px rgba(23, 162, 184, 0);
                }
                100% {
                    box-shadow: 0 0 0 0 rgba(23, 162, 184, 0);
                }
            }
        `;
        document.head.appendChild(style);
    }
});