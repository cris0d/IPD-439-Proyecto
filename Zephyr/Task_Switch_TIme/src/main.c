#include <zephyr/kernel.h>
#include <zephyr/device.h>
#include <zephyr/drivers/gpio.h>

static const struct gpio_dt_spec taskA_pin =
	GPIO_DT_SPEC_GET(DT_PATH(zephyr_user), task1_gpios);
static const struct gpio_dt_spec taskB_pin =
	GPIO_DT_SPEC_GET(DT_PATH(zephyr_user), task2_gpios);

#define STACK_SIZE 512
#define THREAD_PRIORITY 5

K_THREAD_STACK_DEFINE(taskA_stack, STACK_SIZE);
K_THREAD_STACK_DEFINE(taskB_stack, STACK_SIZE);

static struct k_thread taskA_data;
static struct k_thread taskB_data;

void StartTaskA(void *p1, void *p2, void *p3)
{
	while (1) {
		gpio_pin_set_dt(&taskA_pin, 1);
		gpio_pin_set_dt(&taskA_pin, 0);
		k_yield();   /* equivalente a osThreadYield() */
	}
}

void StartTaskB(void *p1, void *p2, void *p3)
{
	while (1) {
		gpio_pin_set_dt(&taskB_pin, 1);
		gpio_pin_set_dt(&taskB_pin, 0);
		k_yield();
	}
}

int main(void)
{

	gpio_pin_configure_dt(&taskA_pin, GPIO_OUTPUT_INACTIVE);
	gpio_pin_configure_dt(&taskB_pin, GPIO_OUTPUT_INACTIVE);

	/* Equivalente a osThreadNew(StartTastkA, ...) */
	k_thread_create(&taskA_data, taskA_stack, STACK_SIZE,
			StartTaskA, NULL, NULL, NULL,
			THREAD_PRIORITY, 0, K_NO_WAIT);

	/* Equivalente a osThreadNew(StartTaskB, ...) */
	k_thread_create(&taskB_data, taskB_stack, STACK_SIZE,
			StartTaskB, NULL, NULL, NULL,
			THREAD_PRIORITY, 0, K_NO_WAIT);

	/* osKernelStart() es implícito en Zephyr: el scheduler ya corre
	   desde el boot, por eso main() puede simplemente retornar */
	return 0;
}