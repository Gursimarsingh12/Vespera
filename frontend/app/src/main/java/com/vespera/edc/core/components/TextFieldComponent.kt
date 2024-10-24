package com.vespera.edc.core.components


import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.text.KeyboardOptions
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.text.input.KeyboardType
import androidx.compose.ui.text.input.VisualTransformation
import androidx.compose.ui.unit.dp

@Composable
fun TextFieldComponent(
    modifier: Modifier = Modifier,
    text: String,
    onValueChange: (String) -> Unit,
    keyboardType: KeyboardType,
    hintText: String,
    errorText: String,
    leadingIcon: ImageVector,
    trailingIcon: ImageVector?,
    onClickTrailingIcon: (() -> Unit)? = null,
    visualTransformation: VisualTransformation,
    isError: Boolean
) {
    OutlinedTextField(
        value = text,
        onValueChange = {
            onValueChange(it)
        },
        modifier = modifier
            .fillMaxWidth(),
        keyboardOptions = KeyboardOptions(
            keyboardType = keyboardType,
        ),
        placeholder = {
            Text(
                text = hintText
            )
        },
        supportingText = {
            Text(
                text = errorText,
            )
        },
        leadingIcon = {
            Icon(imageVector = leadingIcon, contentDescription = "")
        },
        trailingIcon = {
            if (trailingIcon != null) {
                IconButton(
                    onClick = {
                        if (onClickTrailingIcon != null) {
                            onClickTrailingIcon()
                        }
                    },
                ) {
                    Icon(imageVector = trailingIcon, contentDescription = "")
                }
            }
        },
        isError = isError,
        singleLine = true,
        shape = RoundedCornerShape(13.dp),
        visualTransformation = visualTransformation
    )
}