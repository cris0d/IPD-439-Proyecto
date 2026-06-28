#include <zephyr/kernel.h>
#include <zephyr/device.h>
#include <zephyr/drivers/gpio.h>

static const struct gpio_dt_spec isr_pin =
	GPIO_DT_SPEC_GET(DT_PATH(zephyr_user), task1_gpios);

/* Equivalente a B1_Pin -> botón de usuario ya definido en el board file (sw0) */
static const struct gpio_dt_spec button =
	GPIO_DT_SPEC_GET(DT_ALIAS(sw0), gpios);

static struct gpio_callback button_cb_data;

#define STACK_SIZE 512
#define THREAD_PRIORITY 5

K_THREAD_STACK_DEFINE(trigger_stack, STACK_SIZE);
static struct k_thread trigger_data;

/* Equivalente a HAL_GPIO_EXTI_Callback */
void button_isr_callback(const struct device *dev, struct gpio_callback *cb,
			  uint32_t pins)
{
	gpio_pin_set_dt(&isr_pin, 1);
	gpio_pin_set_dt(&isr_pin, 0);
}

/* Solo mantiene el scheduler activo */
void StartTaskTrigger(void *p1, void *p2, void *p3)
{
	while (1) {
		k_msleep(1);   /* equivalente a osDelay(1) */
	}
}

int main(void)
{
	gpio_pin_configure_dt(&isr_pin, GPIO_OUTPUT_INACTIVE);

	/* Configuración del botón como entrada con interrupción falling edge*/
	gpio_pin_configure_dt(&button, GPIO_INPUT | GPIO_PULL_UP);
	gpio_pin_interrupt_configure_dt(&button, GPIO_INT_EDGE_FALLING);

	gpio_init_callback(&button_cb_data, button_isr_callback, BIT(button.pin));
	gpio_add_callback(button.port, &button_cb_data);
	k_thread_create(&trigger_data, trigger_stack, STACK_SIZE,
			StartTaskTrigger, NULL, NULL, NULL,
			THREAD_PRIORITY, 0, K_NO_WAIT);

	return 0;
}

